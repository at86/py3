import asyncio
from aiohttp import web
# from aiohttp_session import get_session, session_middleware
# from aiohttp_session.cookie_storage import EncryptedCookieStorage
# from aiohttp_session import SimpleCookieStorage
# from mysql_pool import POOL
from aiomysql import create_pool
# import time
import wat

M_POOL = None

async def get_pool(loop):
    global M_POOL
    if M_POOL: return M_POOL
    M_POOL = await create_pool(host='127.0.0.1', port=3306, user='root', password='root', db='docs', loop=loop)
    return M_POOL


async def query(request):
    wat.d(1)
    loop = asyncio.get_event_loop()
    pool = await get_pool(loop)
    # print(id(pool))
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT sleep(5);")
            value = await cur.fetchone()
        conn.close()
            # print(value)
    # wat.d(time.time())

    return web.Response(text=str(value))


# app = web.Application(middlewares=[session_middleware(SimpleCookieStorage())])
app = web.Application()
app.router.add_route('GET', '/', query)

web.run_app(app)
