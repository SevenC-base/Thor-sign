#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 2021/08/10 周二  1:03:24.40
# By  Hasaki-h1
import asyncio, aiohttp, time, sys


async def main(url, proxy, params, headers, num, bt):
    tasks = []
    # 限制同时请求的数量pool，可自行调节，默认10个
    pool = 10
    sem = asyncio.Semaphore (pool)

    async with aiohttp.ClientSession () as session:
        for i in range (num):
            tasks.append (control_sem (sem, url=url, proxy=proxy, params=params, headers=headers, session=session, num=i, bt=bt))
        await asyncio.wait (tasks)



async def fetch(url, proxy, params, headers, session, num, bt):
    async with session.get (url=url, proxy=proxy, params=params, headers=headers) as resp:
        text = await resp.text (encoding='UTF-8')
        if resp.status != 200:
            print ('-----------------------------\n✈ 请求失败，状态码为%s' % resp.status)
            end_time = time.time ()
            all_use_time = end_time - bt
            print ('-----------------------------\n✈ 程序运行时长：%s (秒)' % all_use_time)
            sys.exit ()
        if "您已报名 无需再次报名" in text:
            print ('-----------------------------\n✈ 您已报名 无需再次报名')
            end_time = time.time ()
            all_use_time = end_time - bt
            print ('-----------------------------\n✈ 程序运行时长：%s (秒)' % all_use_time)
            sys.exit()




async def control_sem(sem, url, proxy, params, headers, session, num, bt):  # 限制信号量
    async with sem:
        await fetch (url=url, proxy=proxy, params=params, headers=headers, session=session, num=num, bt=bt)


if __name__ == '__main__':
    begin_time = time.time ()

    # 配置雷神众测的项目id值，目前【Vol.397】对应id值为335，依次类推
    id = 335
    # 配置登录认证成功后的token值
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
            ".eyJmbGFnIjoidHJ1ZSIsImV4cCI6MTYyODU5MjY4NCwiaWF0IjoxNjI4NTYzODg0LCJlbWFpbCI6IjExODE1NTEwMzVAcXEuY29tIn0" \
            ".7j-pwWD24Cs-Z52WnqfeFUgUiiza2baaMxybyFGVP7Y "
    # 配置短时间内想要发包的总包数量，如果要调节单位时间内的并发数量请修改pool值
    # 以百度请求为例，3秒可以发100个包，雷神服务器性能肯定更低，大概5000个包就可以了，3分钟之内基本上出现报名审核成功
    # 循环请求总次数num，并发请求次数pool，总的发包数=num*pool
    num = 1000

    # 代理抓包debug, 默认为None
    # Proxy = 'http://127.0.0.1:8080'
    Proxy = None
    Url = 'https://www.bountyteam.com/web/v1/project/hacker/signProject'
    Params = {'id': str (id)}
    Headers = {"Sec-Ch-Ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
               "Accept": "application/json",
               "Acceptlanguage": "zh",
               "Authorization": token,
               "Sec-Ch-Ua-Mobile": "?0",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/92.0.4515.131 Safari/537.36",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Dest": "empty",
               "Referer": "https://www.bountyteam.com/project/detail/" + str (id),
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "close"
               }

    # 运行 loop ，等到 future 完成
    loop = asyncio.get_event_loop ()
    loop.run_until_complete (main (url=Url, proxy=Proxy, params=Params, headers=Headers, num=num, bt=begin_time))
    loop.close ()

