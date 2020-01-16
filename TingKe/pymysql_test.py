import pymysql


def main():
    # 1. 创建数据库连接对象
    con = pymysql.connect(host='192.168.80.128', port=3306,
                          database='ceshi', charset='utf8',
                          user='root', password='hyy123')
    try:
        # 2. 通过连接对象获取游标
        with con.cursor() as cursor:
            # 3. 通过游标执行SQL并获得执行结果
            cursor.execute(
                "select * from log where method like '%e%';"
            )
            result = cursor.fetchall()
            print(result)
    #     with con.cursor() as cursor:
    #         result = cursor.execute("INSERT INTO `log` (`method` ,`url`,`remote_ip` ,`arguments`,`body`,`expend_time` ,`version`, `create_user`) values"
    # "(%s, %s, %s, %s, %s, %s, %s, %s);",
    #                                 ("post","http://127.0.0.1:8888/posttest", "127.0.0.1", str({'name': [b'1', b'3'], 'age': [b'2']}),str(b'',encoding="utf-8"),0.90090, "HTTP/1.1", 12)
    #                                 )
        if result == 1:
            print('添加成功!')
        # 4. 操作成功提交事务
        con.commit()
    finally:
        # 5. 关闭连接释放资源
        con.close()
main()