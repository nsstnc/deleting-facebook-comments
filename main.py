import requests
import json


def get_new_token(cookies):
    # получение нового токена с использованием куки
    pass


def delete_comment(token, comment_id, proxies=None):
    url = f'https://graph.facebook.com/v20.0/{comment_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url, headers=headers, proxies=proxies)
    return response.status_code, response.json()


def clean_comments(post_id, tokens, proxies, cookies):
    for token, cookie, proxy in zip(tokens, cookies, proxies):
        comments = get_comments(post_id, token, proxy)
        for comment in comments:
            status_code, response = delete_comment(token, comment['id'], proxy)
            if status_code == 401:
                new_token = get_new_token(cookie)
                status_code, response = delete_comment(new_token, comment['id'], proxy)
            print(f'Deleted comment {comment["id"]}: {status_code}')


def get_comments(post_id, token, proxies=None):
    url = f'https://graph.facebook.com/v20.0/{post_id}/comments'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []


# Пример использования
post_id = '373194679205134_122099744540369181'
tokens = ['EAAFfDEvgDWIBO8bFgxR8ZBBZCIZBZCu50ZC7Fe7mxe8Kei3fLaYwAfV6ZBgqgQEMnJLNHY4Bg9xlXd1tZAV8t9lTAv3XUfTgPxtGyVZB1q6ORBtDpkd0bCXzp3T5FxOx2IHosLItTFZCiQ0ZBD2K4Kh3rl1WKilqtZC1vrgPFSuVLFdHUcIrC69RMUNkfIf33tyZCgmrR8uB5KT6qjYInbqwqANHwyrh3QZDZD']
proxies = [
    {'http': 'http://164.163.42.27:10000',
     'https': 'http://164.163.42.27:10000'},
    {'http': 'http://181.198.53.6:3128',
     'https': 'http://181.198.53.6:3128'},
]
cookies = ['']

clean_comments(post_id, tokens, proxies, cookies)
