# deleting-facebook-comments
Скрипт для автоматизации удаления комментариев под постами на странице Facebook.

Также реализован дополнительный скрипт Selenium для получения вечного Facebook User Access токена с помощью cookie.

- **Входные  данные**: На вход алгоритм получает ссылки на посты, токены, прокси, cookie.
```python
clean_comments(post_urls, tokens, proxies, cookies)
```

## Стек

- **Backend**: Python, Requests, Selenium
   

## Описание основной части программы

В main.py задаем входные параметры: ссылки на посты, токены, прокси-серверы, куки:
```python
post_urls = [
    'https://www.facebook.com/permalink.php?story_fbid=pfbid032NzMt7pJsH7ek2cZ3FsXo5thnMi6Kyg6Qe2dZfYFpV9KN4RKAuc59xX447RfLg5Ml&id=61561075443726&rdid=AUAXGTL8VK7N1m87',
    'https://www.facebook.com/permalink.php?story_fbid=pfbid02T7aHsauyN69g8vkcX6k4aHxmFCSx2vUHyzvhNyfJdM1iozn9pkGMXYULHXCADD72l&id=61561075443726&rdid=nZBGGFHMxqvpUjEU',
]
proxies = [
    {'http': 'http://103.153.154.6:80',
     'https': 'http://199.167.236.12:3128'},
    {'http': 'http://103.153.154.6:80',
     'https': 'http://199.167.236.12:3128'},
]

# в тестовом режиме подгружаем куки из файла
with open('facebook_cookies.json', 'r') as f:
    cookie = json.load(f)
    cookies = [cookie, cookie]

tokens = [USER_ACCESS_TOKEN, USER_ACCESS_TOKEN]
```
USER_ACCESS_TOKEN для тестирования должен быть записан в config.py. Тестовые Cookie необходимо импортировать с авторизованной
страницы facebook.  

Далее запускается метод clean_comments() из script.py:
```python
def clean_comments(post_urls: List[str], tokens: List[str], proxies: List[Dict], cookies: List[Dict]) -> None:
    """
    Главная функция, которая запускает вспомогательные для удаления ВСЕХ комментарием под переданными постами
    :param post_urls: List[str]
    :param tokens: List[str]
    :param proxies: List[Dict]
    :param cookies: List[Dict]
    :return: None
    """
    for post_url, token, cookie, proxy in zip(post_urls, tokens, cookies, proxies):
        print(post_url, token, cookie, proxy)
        status_code, comments = get_comments(post_url, token, cookie, proxy)

        for comment in comments:
            status_code, response = delete_comment(token, comment['id'], cookie, proxy)

            print(f'Deleted comment {comment["id"]}: {response}')
```

Внутри этот метод для каждого набора данных (пост, токен, куки, прокси) получает все комментарии под постом с помощью: 
``` python
status_code, comments = get_comments(post_url, token, cookie, proxy)
```
После чего каждый комментарий удаляется методом:
``` python
for comment in comments:
   status_code, response = delete_comment(token, comment['id'], cookie, proxy)
```
Также в функционале участвуют дополнительные вспомогательные методы, каждый из которых имеет docstring с описанием работы.


## Файловая структура
```
deleting-facebook-comments/  
├── main.py # Main-файл, отсюда запускаюся скрипты
├── script.py # Основной скрипт удаления и вспомогальые для получения постов и рекламных кампаний
├── selenium_login_and_get_token_by_cookie.py # Доп. метод для получения вечного токена пользователя по его кукам
├── README.md # Документация  
├── requirements.txt # Зависимости  
├── facebook_cookies.json # Cookiе, импортированные с facebook аккаунта
├── config.py # Файл с изначальным токеном
```