import time, asyncio, aiohttp

# python异步编程之asyncio（百万并发） - 三只松鼠 - 博客园 https://www.cnblogs.com/shenh/p/9090586.html
url = 'https://www.qq.com/'
async def hello(url, semaphore):
    print('--------%s' % time.time())
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                s = await response.read()

                # s = str(s, encoding = "utf8") # baidu utf8
                s = str(s, encoding="gbk")  # qq gbk
                # s = bytes.decode(s) # has encoding too

                print('========%s' % time.time(), len(s), s[:8])
                return s


async def run():
    semaphore = asyncio.Semaphore(500)  # 限制并发量为500
    to_get = [hello(url.format(), semaphore) for _ in range(10)]  # 总共1000任务
    await asyncio.wait(to_get)


if __name__ == '__main__':
    #    now=lambda :time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
