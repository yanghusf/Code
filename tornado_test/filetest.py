# coding: utf-8
from typing import Dict, List, Tuple

import tornado.ioloop
import tornado.web
import shutil
import os
import json
import pyexcel as pe


class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(
            """
            <html>
              <head><title>Upload File</title></head>
              <body>
                <form action='file' enctype="multipart/form-data" method='post'>
                <input type='file' name='file'/><br/>
                <input type='submit' value='submit'/>
                </form>
              </body>
            </html>
        """
        )

    def post(self):
        ret = {"result": "OK"}
        upload_path = os.path.join(os.path.dirname(__file__), "files")  # 文件的暂存路径
        print(self.request.files)
        file_metas = self.request.files.get("file", None)  # 提取表单中‘name’为‘file’的文件元数据
        print(file_metas[0].get("filename").split(".")[1])
        # print(bytes(file_metas[0]["body"],"utf8"),">>>>")
        dname = self.get_body_argument("dname", "dname", strip=True)
        content = self.get_body_argument("content", "content", strip=True)
        label = self.get_body_argument("label", "label", strip=True)
        type = self.get_body_argument("type", "type", strip=True)
        sheet = pe.get_sheet(
            file_type=file_metas[0].get("filename").split(".")[1],
            file_content=file_metas[0]["body"],
        )
        if len(sheet) > 100:
            return

        repeat_rows: Dict[str, int] = {}
        rows: List[str] = []
        synthetic_data: List[Tuple] = []
        for index, i in enumerate(sheet.rows()):
            if i[0] not in rows:
                rows.append(i[0])
                synthetic_data.append((dname, i[0], label, type))
            else:
                repeat_rows[i[0]] = repeat_rows.get(i[0], 0) + 1

        strdd = ["%s" for i in range(1, len(sheet))]
        sql = "INSERT  INTO dictionary (`did`, `dname`, `content`, `lable`, `number`,  `type`) values {val}".format(
            val=",".join(strdd)
        )



