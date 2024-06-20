from config import USER_ACCESS_TOKEN
from selenium_login_and_get_token_by_cookie import login_and_get_token_by_cookie
import json
from script import clean_comments, get_all_posts

# посты
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

clean_comments(post_urls, tokens, proxies, cookies)

# login_and_get_token_by_cookie(cookies[0], proxies[0]['https'])

print(get_all_posts(tokens[0], cookies[0], proxies[0]))
