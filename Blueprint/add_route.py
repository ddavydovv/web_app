import requests

# первый запрос (POST)
url = 'http://127.0.0.1:8081/v1/add/tax'
data = {
    'reg_id': 55,
    'tax_rate': 35
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.json())

# второй запрос (GET)
url_1 = 'http://127.0.0.1:8081//v1/fetch/taxes'

response_1 = requests.get(url_1)
print(response_1.status_code)
print(response_1.json())

# третий запрос (GET)
url_2 = 'http://127.0.0.1:8081//v1/fetch/tax'
data_1 = {
    'reg_id': 55
}
response_2 = requests.get(url_2, json=data_1)
print(response_2.status_code)
print(response_2.json())

# четвёртный запрос (GET)

url_3 = 'http://127.0.0.1:8081//v1/fetch/calc'
data_2 = {
    'reg_id': 55,
    'mounth': 10,
    'price': 150
}
response_3 = requests.get(url_3, json=data_2)
print(response_3.status_code)
print(response_3.json())

# пятый запрос (POST)

url_4 = 'http://127.0.0.1:8081//v1/update/tax'
data_3 = {
    'reg_id': 55,
    'tax_rate': 7,
}
response_4 = requests.post(url_4, json=data_3)
print(response_4.status_code)
print(response_4.json())
