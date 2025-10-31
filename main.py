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
base_value = {'RUB', 'EUR', 'USD'}

base_url = f'https://data.fixer.io/api/latest?access_key={TOKEN}'

class CreateUser:

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
        count_for_buy = int(input(f'Какое количество {user_data['user_buy']} купить?: '))
        if count_for_buy >= 1:
            respons = loads(httpx.get(base_url).content)
            user_value = respons['rates'][user_data['user_value']]
            user_buy_value = respons['rates'][user_data['user_buy']]
            if user_data['user_buy'] == 'EUR':
                payment_cost = ((user_value * user_buy_value) * count_for_buy)  * 1.03
                commission = payment_cost * 0.03
                print(f'К оплате {payment_cost:.2f} {user_data['user_value']}, комиссия составила: {commission:.2f} {user_data['user_value']}')
            else:
                print(user_value)
                print(user_buy_value)
                payment_cost = count_for_buy * (user_value / user_buy_value)
                commission = payment_cost * 0.03
                print(f'К оплате {payment_cost:.2f} {user_data['user_value']}, комиссия составила: {commission:.2f} {user_data['user_value']}')
        else:
            print('Число должно быть > 0')

    def delete_user(self):
        user_for_delete = redis_client.delete('user:1')
        base_value.update(['RUB', 'EUR', 'USD'])
        print('Пользователь удален')

        
async def main():

    while True:

        print('==========================')
        print('''1 | Создать пользователя\n2 | Купить валюту\n3 | Все пользователи\n4 | Удалить пользователя\n0 | Выйти''')
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
            
            case 4:
                CreateUser().delete_user()

            case 0:
                print('Вы вышли из программы')
                break

            case _:
                print('Я тебя не понимаю')



if __name__ == '__main__':
    asyncio.run(main())