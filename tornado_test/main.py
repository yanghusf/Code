import asyncio
import os

import tornado.ioloop
import tornado.web

import aiomysql

from conf.setting import MYSQL
from tornado_test.filehandler import FileUploadHandler, NodeSearchManager, TacticsManager, \
    GetTacticsInfo, UpdateTacticsContent
from tornado_test.mysql.mysqlDB import init_db, Database


class Config(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool




class ScanRestApi(tornado.web.RequestHandler):
    def prepare(self):
        print(self.request.method)
        # param = self.request.body.decode("utf8")
        # param = json.loads(param)
        # print(self.request.query)


class MindHandler(ScanRestApi):
    async def get(self):
        # print(self.get_argument('name'))
        # print("GET expend_time:",self.request.request_time())
        # print("GET full_url:",self.request.full_url(),type(self.request.full_url()))
        # print("GET remote_ip:",self.request.remote_ip)
        # print("GET uri:",self.request.uri)
        # print("GET arguments:",self.request.arguments)
        #
        # print("GET version:",self.request.version)
        # print("GET get_status:",self.request.get_status())
        # print("GET query:",self.request.query)
        # print("GET headers:",self.request.headers)
        # print("GET headers:", self.request.headers['host'])
        print("GET body:",self.request.body)
        # print("GET body_arguments:",self.request.body_arguments)
        # async with self.db_pool.acquire() as conn:
        #     async with conn.cursor(aiomysql.DictCursor) as cur:
        #         await cur.execute("select * from log")
        #         token = await cur.fetchone()
        #         print(token)
        self.write("Hello World")

class PostMindHandler(ScanRestApi):
    def post(self):
        print("POST remote_ip:", self.request.remote_ip,type(self.request.remote_ip))
        print(self.request.method,type(self.request.method))
        print("POST expend_time:", self.request.request_time(),type(self.request.request_time()))
        print("POST arguments:", self.request.arguments, type(self.request.arguments))
        print("POST full_url:", self.request.full_url(),type(self.request.full_url()))
        print("POST body_arguments:", self.request.body_arguments, type(self.request.body_arguments))
        print("POST headers:", self.request.headers,type(self.request.headers))
        print("POST body:", self.request.body,type(self.request.body))
        print("POST files:", self.request.files)
        print("GET version:",self.request.version, type(self.request.version))

    def put(self):
        print("put arguments:", self.request.arguments, type(self.request.arguments))
        print("put full_url:", self.request.full_url())
        print("put body_arguments:", self.request.body_arguments)
        print("put headers:", self.request.headers)
        print("put query:", self.request.query)
        print("put expend_time:", self.request.request_time())
        print("put body:", self.request.body,type(self.request.body))

    def patch(self):
        print("patch arguments:", self.request.arguments, type(self.request.arguments))
        print("patch full_url:", self.request.full_url())
        print("patch body_arguments:", self.request.body_arguments)
        print("patch headers:", self.request.headers)
        print("patch query:", self.request.bodyquest.query)
        print("patch expend_time:", self.request.request_time())
        print("patch body:", self.request.body,type(self.request.body))

    def delete(self):
        print("delete arguments:", self.request.arguments, type(self.request.arguments))
        print("delete full_url:", self.request.full_url())
        print("delete body_arguments:", self.request.body_arguments)
        print("delete headers:", self.request.headers)
        print("delete query:", self.request.query)
        print("delete expend_time:", self.request.request_time())
        print("delete body:", self.request.body,type(self.request.body))
    def head(self):
        print("delete full_url:", self.request.full_url())
        print("delete body_arguments:", self.request.body_arguments)

class TestHandler(ScanRestApi):
    async def get(self):
        # a = self.request.query
        # print(a)
        # b = self.get_argument('name')
        #
        # print(b,type(b))
        # import urllib.parse
        # c = urllib.parse.unquote(b)
        # print(c)
        b = self.get_argument('id')
        print(b,type(b))





applaction = tornado.web.Application([
    (r"/index", MindHandler),
    (r"/posttest", PostMindHandler),
    (r"/test",TestHandler),
    (r"/file",FileUploadHandler),
    (r"/node",NodeSearchManager),
    (r"/tactics",TacticsManager),
    (r"/tactics/info",GetTacticsInfo),
    (r"/tactics/update/content", UpdateTacticsContent)

])



if __name__ == '__main__':

    applaction.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
