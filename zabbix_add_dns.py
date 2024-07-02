import requests
import json


# Заголовки запроса
HEADERS = {
        'Content-Type': 'application/json-rpc'
}

def create_host(dns_address, url, token, headers):
    """Основная функция реализующая создания хоста."""

    # JSON-запрос для создания хоста
    request_data = {
        'jsonrpc': '2.0',
        'method': 'host.create',
        'params': {
            'host': dns_address,
            'interfaces': [
                {
                    'type': 1,
                    'main': 1,
                    'useip': 0,
                    'ip': '',
                    'dns': dns_address,
                    'port': '10050'
                }
            ],
            'groups': [
                {'groupid': 2}
            ],
            'templates': [
                {
                    'templateid': '10564'
                }
            ],
        },

        'id': 1,
        'auth': token
    }

    # Отправка запроса на создание хоста
    response = requests.post(url, data=json.dumps(request_data), headers=headers)

    # Обработка ответа и вывод информации
    if response.status_code == 200:
        response_data = response.json()
        if 'error' in response_data:
            print('Ошибка API:', response_data['error'])
        elif 'result' in response_data:
            host_id = response_data['result']['hostids'][0]
            print(f'Хост {dns_address} успешно создан с ID: {host_id}')
    else:
        print('Ошибка HTTP:', response.status_code, response.reason)


# запрос необходимых данных
url = input('Введите url zabbix, вида: http://127.0.0.1/api_jsonrpc.php: ')
username = input('Введите имя пользователя zabbix: ')
password = input('Введите пароль пользователя zabbix: ')

# получение токена
get_token = requests.post(url,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "username": username,
                          "password": password},
                      "id": 1
                  })
token = get_token.json()["result"]


# считывание IP адресов из файла
dns_addresses = []
with open('hosts_dns.txt', 'r') as file:
    for line in file:
        dns_addresses.append(line.strip())

# создание хостов для каждого IP адреса
for dns_address in dns_addresses:
    create_host(dns_address, url, token, HEADERS)