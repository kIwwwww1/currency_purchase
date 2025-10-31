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

    # def __init__(self) -> None:
    #     self.user_id = None
    #     self.name = None
    #     self.user_value = None

    def create_user(self):
        user_in_redis = redis_client.get(name='user:1') # Здесь написано постоянное значение "user:1" (что нельзя делать), 
        # но я решил так сделать потому что мы не работаем с бд и у нас гарантировано будет только 1 пользователь в терминале

        if user_in_redis:
            return f'У вас уже есть пользователь {user_in_redis}'
        user_id = len(data) + 1
        user_name = input('Введите имя пользователя "Кирилл": ')
        try:
            user_value = input(f'Укажите свою валюту {base_value}: ').upper()
            if user_value not in base_value:
                print(f'Вы ввели не верные данные, пожалуйста начните заново')
            base_value.remove(user_value)
            user_buy = input(f'Укажите покупаемую валюту {base_value}: ').upper()
            if user_buy not in base_value:
                print(f'Вы ввели не верные данные, пожалуйста начните заново')
            user_data = {
                'id': user_id,
                'name': user_name,
                'user_value': user_value,
                'user_buy': user_buy,
            }
            redis_client.set(name=f'user:{user_id}' ,value=dumps(user_data))
            data.append(user_data)
            print('Данные добавлены')
        except Exception:
            print('Произошла ошибка')

    def buy_value(self):
        user_data = loads(redis_client.get(name='user:1'))
        print(user_data)

        count_for_buy = int(input(f'Какое количество {user_data} купить?'))
        r = httpx.get(base_url)
        print(r.content)


# async def buy_value():
#     async with httpx.AsyncClient() as client:
#         r = await client.get(base_url)
#         print('Получили данные')
#         return loads(r.content)
        
async def main():

    while True:
        print('==========================')
        print('''1 | Создать пользователя\n2 | Купить валюту\n3 | Все пользователи\n0 | Выйти''')
        print('==========================')

        user_map =  int(input('Выберите пункт: '))
        print('==========================')

        match user_map:
            case 1:
                print(CreateUser().create_user())
                
            case 2:
                print(CreateUser().buy_value())
                
            case 3:
                user_in_redis = redis_client.get('user:1')
                if user_in_redis:
                    print(loads(user_in_redis))
                else:
                    print(data) if len(data) >= 1 else print('В базе пусто')
            case 0:
                print('Вы вышли из программы')
                break
            case _:
                print('Я тебя не понимаю')



if __name__ == '__main__':
    asyncio.run(main())