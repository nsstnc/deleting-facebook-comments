import requests
import json

import urllib.parse
from config import ACCESS_TOKEN

def extract_ids(url):
    # разбираем url поста на параметры
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # получаем id поста и id страницы
    story_fbid = query_params.get('story_fbid', [None])[0]
    page_id = query_params.get('id', [None])[0]
    print(story_fbid, page_id)
    return story_fbid, page_id


def get_new_token(cookies):
    # получение нового токена с использованием куки
    pass



def delete_comment(token, comment_id, proxies=None):
    url = f'https://graph.facebook.com/v20.0/{comment_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url, headers=headers, proxies=proxies, timeout=30)
    return response.status_code, response.json()


def clean_comments(post_urls, tokens, proxies, cookies):
    for post_url, token, cookie, proxy in zip(post_urls, tokens, cookies, proxies):
        status_code, comments = get_comments(post_url, token, proxy)

        if status_code == 401:
            new_token = get_new_token(cookie)
            status_code, comments = get_comments(post_url, new_token, proxy)


        for comment in comments:
            status_code, response = delete_comment(token, comment['id'], proxy)
            if status_code == 401:
                new_token = get_new_token(cookie)
                status_code, response = delete_comment(new_token, comment['id'], proxy)
            print(f'Deleted comment {comment["id"]}: {status_code}')


# получение всех комментариев к посту
def get_comments(post_url, token, proxies=None):
    post_id, page_id = extract_ids(post_url)
    url = f'https://graph.facebook.com/v20.0/{page_id}_{post_id}/comments'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers, proxies=proxies, timeout=30)

    return response.status_code, response.json()['data']



# метод для получения всех постов со страницы
def get_all_posts(token, proxies=None):
    url = f'https://graph.facebook.com/v20.0/me/posts'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers, proxies=proxies, timeout=30)

    return response.status_code, response.json()['data']



post_urls = ['https://www.facebook.com/permalink.php?story_fbid=pfbid032NzMt7pJsH7ek2cZ3FsXo5thnMi6Kyg6Qe2dZfYFpV9KN4RKAuc59xX447RfLg5Ml&id=61561075443726&rdid=AUAXGTL8VK7N1m87']
tokens = [ACCESS_TOKEN]
proxies = [
    {'http': 'http://103.153.154.6:80',
     'https': 'http://199.167.236.12:3128'}
]
cookies = ['']

clean_comments(post_urls, tokens, proxies, cookies)

print(get_all_posts(ACCESS_TOKEN, proxies[0]))
