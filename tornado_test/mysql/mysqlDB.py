import logging
import aiomysql
import traceback


class Database(object):
    def __init__(self, pool):
        self.pool = pool

    async def query(self, sql, *args):
        try:
            logging.info("Database query sql【%s】 args【%s】", sql, args)
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql, args)
                    value = await cur.fetchone()
                    return value
        except Exception as e:
            exe = traceback.format_exc()
            logging.error(exe)
            logging.error("query error SQL 【%s】 args【%s】" % (sql,args))
            return {}

    async def find(self, sql, *args):
        try:
            logging.info("Database find sql【%s】 args【%s】", sql, args)
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql, args)
                    value = await cur.fetchall()
                    return value
        except Exception as e:
            exe = traceback.format_exc()

            logging.error(exe)
            logging.error("find error SQL 【%s】args【%s】" % (sql,args))
            return []

    async def update(self, request, sql, *args):
        '''更新'''
        status = await self.__execute(request, sql, *args)
        return status

    async def insert(self, request, sql, *args):
        '''更新'''
        status = await self.__execute(request, sql, *args)
        return status

    async def delete(self, request, sql, *args):
        '''更新'''
        status = await self.__execute(request, sql, *args)
        return status

    # def __getattr__(self, item):
    #     if item in ('update', 'insert', 'delete'):
    #         setattr(self, item, self.__execute)
    #         return getattr(self, item)

    async def __execute(self, request, sql, *args):

        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql, args)
                    if cur.lastrowid == 0:
                        return True
                    return cur.lastrowid
        except Exception as e:
            exe = traceback.format_exc()
            logging.error(exe)
            logging.error("request error SQL 【%s】args【%s】" % (sql,args))
            return False

async def init_db(loop, config):

    pool = await aiomysql.create_pool(host=config['host'], port=config["port"],
                                      user=config["user"], password=config["password"],
                                      db=config["db"], minsize=config["minsize"],
                                      maxsize=config["maxsize"], pool_recycle=7 * 3600,
                                      loop=loop, autocommit=True)

    return Database(pool)

