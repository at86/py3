import asyncio
from aiohttp import web
# from aiohttp_session import get_session, session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
# from aiohttp_session import SimpleCookieStorage

import pymysql
# import time
import wat

async def query(request):
    wat.d(1)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='docs', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT sleep(5);")
    value = cursor.fetchone()
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return web.Response(text=str(value))


# app = web.Application(middlewares=[session_middleware(SimpleCookieStorage())])
app = web.Application()
app.router.add_route('GET', '/', query)

web.run_app(app)
