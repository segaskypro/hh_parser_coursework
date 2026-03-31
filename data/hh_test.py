import requests

# ID компании Яндекс
employer_id = 1740

# Получаем информацию о компании
url = f"https://api.hh.ru/employers/{employer_id}"
response = requests.get(url)
company = response.json()

print("Название:", company['name'])
print("Сайт:", company.get('site_url', 'нет сайта'))
