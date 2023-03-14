import asyncio
import sys
import platform
from datetime import datetime,timedelta
import aiohttp
from pprint import pprint


BASE_URL='https://api.privatbank.ua/p24api/exchange_rates?date='


def url_gen(day=None) -> list: #day = 0 , 1, ,2
    url_list = []
    today = datetime.now().date()
    if day:
        for i in range(day):  # i >= 1
            local_day = today-timedelta(days=i)
            local_day_url = BASE_URL+local_day.strftime('%d.%m.%Y')
            url_list.append(local_day_url)
        return url_list
    else:
        today_url = BASE_URL+today.strftime('%d.%m.%Y')
        url_list.append(today_url)
    return url_list


async def main(urls, add_curency= None):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            print(f'Starting {url}')
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        res = await response.json()
                        leng = len(res['exchangeRate'])
                        for elem in range(leng):
                            if res['exchangeRate'][elem]['currency'] in ['USD', 'EUR', add_curency]:
                                print(res['date'], res['exchangeRate'][elem])
                    else:
                        print(f'Error status: {response.status}')
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}, {err} ')


if __name__ == '__main__':

    sys_argv_len = len(sys.argv)

    if sys_argv_len == 1:
        days = 0
        ad_cur = None
    elif sys_argv_len == 2:
        days = sys.argv[1]
        ad_cur = None
    elif sys_argv_len == 3:
        days = sys.argv[1]
        ad_cur = sys.argv[2]
    else:
        print('Please provide correct days number. One number up to 10')
        exit()

    if int(days) > 10:
        print(f'You can see currency only up to 10 previous days')
        exit()
    else:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main(url_gen(int(days)), ad_cur))