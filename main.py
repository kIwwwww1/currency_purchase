import redis
import asyncio
import httpx
from json import loads, dumps
from dotenv import load_dotenv
from os import getenv

redis_client = redis.Redis(decode_responses=True)

load_dotenv()

TOKEN = getenv('TOKEN')

data = []
base_value = ['РУБ', 'EUR', 'USD']

base_url = f'https://data.fixer.io/api/latest?access_key={TOKEN}'

class CreateUser:

    def __init__(self) -> None:
        self.user_id = None
        self.name = None
        self.user_value = None

    def create_user(self):
        user_in_redis = redis_client.get(name='user:1') # Здесь написано постоянное значение "user:1" (что нельзя делать), 
        # но я решил так сделать потому что мы не работаем с бд и у нас гарантировано будет только 1 пользователь в терминале

        if user_in_redis:
            return f'У вас уже есть пользователь {user_in_redis}'
        user_id = len(data) + 1
        user_name = input('Введите имя пользователя "Кирилл": ')
        user_value = input('Укажите свою валюту "РУБ", "EUR"", "USD": ').upper()
        if user_value not in base_value:
            return f'Вы ввели не верные данные, пожалуйста начните заново'
        user_data = {
            'id': user_id,
            'name': user_name,
            'user_value': user_value,
        }
        redis_client.setex(name=f'user:{user_id}' ,time=25 ,value=dumps(user_data))
        data.append(user_data)
        return 'Данные добавлены'
    

async def main_func(self):
    async with httpx.AsyncClient() as client:
        print('Получаем данные...')
        r = await client.get(base_url)
        print('Получили данные')
        return loads(r.content)
        
async def main():

    # 1 Создать пользвателя
    # 2 Указать валюту пользователя
    # 3 Все пользователи

    while True:
        user_map =  int(input('Выберите пункт: '))

        match user_map:
            case 1:
                print(CreateUser().create_user())
                
            case 2:
                pass
                
            case 3:
                print(data)



if __name__ == '__main__':
    asyncio.run(main())