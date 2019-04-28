import time
import asyncio

# # 定义异步函数 python异步编程之asyncio（百万并发） - 三只松鼠 - 博客园 https://www.cnblogs.com/shenh/p/9090586.html
# async def hello():
#     # atdo err
#     # async with asyncio.sleep(1):
#     #     print('Hello World:%s' % time.time())
#
#     await asyncio.sleep(1)
#     print('Hello World:%s' % time.time())
#
# def run():
#     for i in range(5):
#         loop.run_until_complete(hello())
#
# loop = asyncio.get_event_loop()
# if __name__ =='__main__':
#     run()


# https://github.com/michaelliao/learn-python3/blob/master/samples/async/async_hello.py
#
async def hello():
    print('----------:%s' % time.time())
    await asyncio.sleep(1)
    print('==========:%s' % time.time())

if __name__ =='__main__':
    loop = asyncio.get_event_loop()
    tasks=[]
    for i in range(5):
        tasks.append(hello())

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
