import asyncio
import httpx
from json import loads, dumps
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('TOKEN')

base_value = ['РУБ', 'EUR', 'USD']

base_url = f'https://data.fixer.io/api/latest?access_key={TOKEN}'

def from_what_urrency():
    user_value = input('Укажите свою валюту: ')


async def main_func():
    async with httpx.AsyncClient() as client:
        print('Получаем данные...')
        r = await client.get(base_url)
        print('Получили данные')
        return loads(r.content)


if __name__ == '__main__':
    from_what_urrency()