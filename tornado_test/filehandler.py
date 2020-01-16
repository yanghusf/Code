# coding: utf-8
from typing import Dict, List, Tuple

import aiomysql
import tornado.web
import json
import pyexcel as pe

from tornado_test import warehouse, response_code


class FileUploadHandler(tornado.web.RequestHandler):
    def set_default_header(self):
        print("setting headers!!!")
        self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        # self.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
    async def get(self):

        # async with aiomysql.create_pool(
        #     host="192.168.80.128",
        #     port=3306,
        #     user="root",
        #     password="hyy123",
        #     db="ceshi",
        #     autocommit=True,
        # ) as pool:
        #     async with pool.acquire() as conn:
        #         async with conn.cursor() as cur:
        #             await cur.execute(
        #             warehouse.UPDATE_DICTIONARY,{"did":2, "dictionary_type":0})
        #             dictionary_obj_content = await cur.fetchone()
        #             print(dictionary_obj_content)

        # test_args = self.get_arguments('test_arg[]', '')  # 获取到list
        # print(test_args,">>>>")
        self.write(
            """
<html>
  <head><title>Upload File</title>
  <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
  </head>
  <body>
    <form action='file' enctype="multipart/form-data" method='post'>
    <input type="text" id="taskName" name="taskName" maxlength="40"><br/>
    <textarea rows="3" cols="20" id ="texte">
在w3school，你可以找到你所需要的所有的网站建设教程。
</textarea><br/>
    <input type='file' name='file' id='crowd_file'/><br/>
    <input type='submit' value='submit'/>
  
    <button type="button" id='submit'>Click Me!</button>
    </form>
  </body>
  <script type="text/javascript">
$('#submit').click(function () {

    var crowd_name =$('#taskName').val();
    var content =$('#texte').val();
    
    var crowd_file = $('#crowd_file')[0].files[0];
    
    var formData = new FormData();

    formData.append("file",$('#crowd_file')[0].files[0]);
    formData.append("dname", crowd_name);
    formData.append("type", 0);
    formData.append("content", content);
    var list_data = {'test_arg': ['v1', 'v2']} 
    formData.append("list_data", list_data);
    console.log(formData)

    $.ajax({
        url:'/file',
        
        type:'PUT',
        async: false,
        data: formData,
        contentType: false,
        processData: false,
        success: function(data){
            console.log(data);
            if (data.status == 'ok') {
                alert('上传成功！');
            }

        },
        error:function(response){
            console.log(response);
        }
    });

})
</script>
</html>
"""
        )

    async def post(self,) -> None:
        """
        字典提交
        :return:
        """
        try:
            dictionary_name = self.get_body_argument("dname", strip=True)

            content = self.get_body_argument("content", "", strip=True)
            label = self.get_body_argument("label", "", strip=True)
            dictionary_type = self.get_body_argument("type", strip=True)
            file_metas = self.request.files.get("file")

        except (ValueError, KeyError, AssertionError):
            return await self.finish({"code": "234"})
        if not content and not file_metas:
            return await self.finish({"code": "234"})

        label = json.dumps(label)

        repeat_rows: Dict[str, int] = {}
        rows: List[str] = []
        if content:
            """有内容的情况下不读取提交文件"""
            file_metas = None
            content_list = content.split("\n")
            if len(content_list) > 1000:
                return await self.finish({"code": 2, "msg": "超过数量限制"})
            for index, i in enumerate(content_list):
                if i not in rows:
                    rows.append(i)
                else:
                    repeat_rows[i] = repeat_rows.get(i, 0) + 1
        if file_metas:
            filename = file_metas[0].get("filename")
            if filename:
                file_suffix = filename.split(".")[1]
            else:
                return await self.finish({"code": 2, "msg": "请检查文件后缀"})
            sheet = pe.get_sheet(
                file_type=file_suffix, file_content=file_metas[0]["body"]
            )
            if len(sheet) > 1000:
                return await self.finish({"code": 2, "msg": "数量不能大于1000"})

            for index, i in enumerate(sheet.rows()):
                if index == 0:
                    continue
                if i[0] not in rows:
                    rows.append(i[0])
                else:
                    repeat_rows[i[0]] = repeat_rows.get(i[0], 0) + 1
        repeated_count = sum(list(repeat_rows.values()))
        async with aiomysql.create_pool(
            host="192.168.80.128",
            port=3306,
            user="root",
            password="hyy123",
            db="ceshi",
            autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        warehouse.Dictionary_INSERT,
                        {
                            "dname": dictionary_name,
                            "content": json.dumps(rows),
                            "label": label,
                            "type": dictionary_type,
                        },
                    )

        return await self.finish({"code": 0, "repeated_count": repeated_count})


    async def put(self) -> None:
        """
        修改字典内容
        :param manager_id:
        :return:
        """
        try:
            did = self.get_argument("did", strip=True)
            dictionary_type = self.get_argument("type")
            content = self.get_argument("content", "", strip=True)
            file_metas = self.request.files.get("file")

        except (ValueError, KeyError, AssertionError):
            return await self.finish(
                {"code": response_code.ParameterError, "msg": "获取参数错误"}
            )
        if not content and not file_metas:
            return await self.finish(
                {"code": response_code.ParameterError, "msg": "没有字典项和文件"}
            )
        repeat_rows: Dict[str, int] = {}
        rows: List[str] = []
        if content:
            """有内容的情况下不读取提交文件"""
            file_metas = None
            content_list = content.split("\n")
            if len(content_list) > 1000:
                return await self.finish(
                    {"code": response_code.ParameterError, "msg": "超过数量限制"}
                )
            for index, i in enumerate(content_list):
                if i not in rows:
                    rows.append(i)
                else:
                    repeat_rows[i] = repeat_rows.get(i, 0) + 1
        if file_metas:
            filename = file_metas[0].get("filename")
            if filename:
                file_suffix = filename.split(".")[1]
            else:
                return await self.finish(
                    {"code": response_code.ParameterError, "msg": "请检查文件后缀"}
                )
            sheet = pe.get_sheet(
                file_type=file_suffix, file_content=file_metas[0]["body"]
            )
            if len(sheet) > 1000:
                return await self.finish(
                    {"code": response_code.ParameterError, "msg": "数量不能大于1000"}
                )

            for index, i in enumerate(sheet.rows()):
                if i[0] not in rows:
                    rows.append(i[0])
                else:
                    repeat_rows[i[0]] = repeat_rows.get(i[0], 0) + 1
        repeated_count = sum(list(repeat_rows.values()))

        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        warehouse.UPDATE_DICTIONARY["get_dictionary"],
                        {"did": did, "dictionary_type": dictionary_type},
                    )
                    dictionary_obj = await cur.fetchone()
                    print(dictionary_obj,">>>")
                    try:
                        list_dictionary_content = json.loads(dictionary_obj[2])
                    except (ValueError, KeyError, AssertionError):
                        return await self.finish(
                            {"code": response_code.ParameterError, "msg": "解析字典错误"}
                        )
                    print("*"*120)
                    print(list_dictionary_content,type(list_dictionary_content))
                    print(rows,type(rows))
                    list_dictionary_content.extend(rows)
                    new_dictionary_content = list(set(list_dictionary_content))
                    await cur.execute(
                        warehouse.UPDATE_DICTIONARY["update_dictionary"],
                        {
                            "content": json.dumps(new_dictionary_content),
                            "dtype": dictionary_type,
                            "dictionary_count": len(new_dictionary_content),
                            "did": did,
                        },
                    )
        return await self.finish({"code": 0, "repeated_count": repeated_count})


class NodeSearchManager(tornado.web.RequestHandler):
    async def get(self) -> None:
        """
        查询获取所有节点队列信息
        :return:
        """
        try:
            page = abs(int(self.get_argument("page", "1")))
            step = abs(int(self.get_argument("step", "20")))
            search = self.get_argument("search", "")
            node_state = self.get_argument("node_state", "")
            print(node_state,type(node_state))
            start = (page - 1) * step
        except (ValueError, TypeError):
            return await self.finish({"code": response_code.ParameterError})
        *k, search = search.split(":", 1)
        key = (
            {"ip": "node_ip", "hex": "node_name"}.get(k[0], "remarks")
            if k
            else "remarks"
        )
        # search = search.replace("'", "").replace('"', "").replace("%", "")
        # search = search[1:] if search.startswith("$") else f"%{search}"
        # search = search[:-1] if search.endswith("$") else f"{search}%"
        search = f"{search}%"
        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(
                    aiomysql.DictCursor, aiomysql.cursors.DeserializationCursor
                ) as cur:
                    if not node_state:
                        search_sql = warehouse.GET_NODE_SEARCH_MANAGER[
                            "not_a_state"
                        ].format(key=key)
                        await cur.execute(
                            search_sql, {"start": start, "step": step, "search": search}
                        )
                    else:
                        search_sql = warehouse.GET_NODE_SEARCH_MANAGER["yes_state"].format(
                            key=key
                        )
                        print(search_sql,">>>>>")
                        await cur.execute(
                            search_sql,
                            {
                                "start": start,
                                "step": step,
                                "search": search,
                                "node_state": node_state,
                            },
                        )
                    data = await cur.fetchall()
        return await self.finish({"code": 0, "data": data})




class TacticsManager(tornado.web.RequestHandler):
    """
    技战法管理器
    """
    async def get(self) -> None:
        """
        根据字典type值获取相关字典数据，动态资源
        :param manager_id:
        :return:
        """
        try:
            page = abs(int(self.get_argument("page", "1")))
            step = abs(int(self.get_argument("step", "20")))
            start = (page - 1) * step
        except (ValueError, KeyError):
            return await self.finish({"code": response_code.ParameterError})
        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(warehouse.GET_TACTICS_COUNT)
                    count = await cur.fetchone()
                    await cur.execute(
                        warehouse.GET_TACTICS,
                        {"start": start, "step": step},
                    )
                    dictionary = await cur.fetchall()

                return await self.finish({"code": 0, "dictionary": dictionary, **count})

    async def post(self) -> None:
        """
        添加技战法处理
        :return:
        """

        try:
            classification = self.get_body_argument("classification", strip=True)
            name = self.get_body_argument("tactics_name", strip=True)
            content = self.get_body_argument("tactics_content", "", strip=True)
            description = self.get_body_argument("describe", "", strip=True)
        except (ValueError, KeyError, AssertionError):
            return await self.finish(
                {"code": response_code.ParameterError, "msg": "获取参数错误"}
            )

        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(warehouse.INSERT_TACTICS,{"classification": classification,"name": name,"content": content,"description": description,})
        return await self.finish({"code": 0})

    async def put(self) -> None:
        """
        修改技战法
        :param manager_id:
        :return:
        """
        try:
            tid = self.get_argument("tid", strip=True)
            classification = self.get_argument("classification", strip=True)
            name = self.get_argument("tactics_name", strip=True)
            description = self.get_argument("describe", "", strip=True)
            activate_groups = self.get_arguments("activate_groups", strip=True)
            tcontent = self.get_arguments("tcontent", strip=True)
            print(tcontent,type(tcontent),",,,")
        except (ValueError, KeyError, AssertionError):
            return await self.finish(
                {"code": response_code.ParameterError, "msg": "获取参数错误"}
            )
        tactics_group_relation_list = [ (tid,i) for i in activate_groups]
        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(warehouse.UPDATE_TACTICS['update_tactics'],{"tid": tid,"classification": classification,"name": name,"description": description})
                    # 先删除技战法和组的关系然后插入
                    await cur.execute(warehouse.UPDATE_TACTICS['delete_tactics_group_relation'],{"tid": tid})
                    print(">>>>>>")
                    print(tactics_group_relation_list)
                    await cur.executemany(warehouse.UPDATE_TACTICS["insert_tactics_group_relation"],tactics_group_relation_list)
        return await self.finish({"code": 0})


class GetTacticsInfo(tornado.web.RequestHandler):
    """
    获取技战法用户组数据
    """

    async def get(self) -> None:
        """
        获取组列表，动态资源
        :param manager_id:
        :return:
        """
        try:
            id = self.get_argument("tid")

        except (ValueError, KeyError):
            return await self.finish({"code": response_code.ParameterError})

        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(warehouse.VIEW_TACTICS['get_tactics_obj'],{"id": id})
                    tactics_obj = await cur.fetchone()
                    await cur.execute(warehouse.VIEW_TACTICS['get_tactics_groups'])
                    groups = await cur.fetchall()
                    await cur.execute(
                        warehouse.VIEW_TACTICS['get_tactics_group_relation'], {"id": id})
                    activate_group = await cur.fetchall()
        return await self.finish({"code": 0, "groups": groups, "tactics_obj":tactics_obj, "activate_group":activate_group})

class UpdateTacticsContent(tornado.web.RequestHandler):
    """
    技战法修改内容
    """

    async def put(self) -> None:
        """
        修改技战法content信息，动态资源
        :param manager_id:
        :return:
        """
        try:
            id = self.get_argument("tid")
            # content = self.get_argument("tactics_content")
            content = self.get_arguments("tactics")
            print(id)
            print(content)

        except (ValueError, KeyError):
            return await self.finish({"code": response_code.ParameterError})
        async with aiomysql.create_pool(
                host="192.168.80.128",
                port=3306,
                user="root",
                password="hyy123",
                db="ceshi",
                autocommit=True,
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(warehouse.UPDATE_TACTICS_CONTENT, {"id": id, "content": json.dumps(content)})

        return await self.finish({"code": 0})


