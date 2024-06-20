import requests
import urllib.parse
from typing import List, Dict


def extract_ids(url: str) -> (str, str):
    """
    Достаем из ссылки id поста и id страницы
    :param url: str
    :return: str
    """
    # разбираем url поста на параметры
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # получаем id поста и id страницы
    story_fbid = query_params.get('story_fbid', [None])[0]
    page_id = query_params.get('id', [None])[0]
    print(story_fbid, page_id)
    return story_fbid, page_id


def delete_comment(token: str, comment_id: str, cookies: Dict, proxies: List = None) -> str or (str, Dict):
    """
    Удаление комментария по его идентификатору
    :param token: str
    :param comment_id: str
    :param cookies: Dict
    :param proxies: List = None
    :return:
    """
    url = f'https://graph.facebook.com/v20.0/{comment_id}'
    status_code, response = get_page_access_token(token, cookies, proxies)
    if status_code == 200:
        page_access_token = response['data'][0]['access_token']
        headers = {
            'Authorization': f'Bearer {page_access_token}',
        }
        # Преобразование куки в формат, используемый requests
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        response = requests.delete(url, headers=headers, proxies=proxies, cookies=cookies_dict, timeout=30)
        return response.status_code, response.json()
    return f"Cannot delete comment: {response}"


def get_comments(post_url: str, token: str, cookies: Dict, proxies: List = None) -> (str, List[Dict]):
    """
    Получение всех комментариев к посту
    :param post_url: str
    :param token: str
    :param cookies: Dict
    :param proxies: List=None
    :return: (str, List[Dict])
    """
    post_id, page_id = extract_ids(post_url)

    url = f'https://graph.facebook.com/{page_id}_{post_id}/comments'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Преобразование куки в формат, используемый requests
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    response = requests.get(url, headers=headers, cookies=cookies_dict, proxies=proxies, timeout=30)
    print(response.json())
    return response.status_code, response.json()['data']


def get_page_access_token(user_access_token: str, cookies: Dict, proxies: List = None) -> (str, Dict):
    """
    Получение токена ПЕРВОЙ страницы из списка страниц, к которым пользователь имеет доступ
    :param user_access_token: str
    :param cookies: Dict
    :param proxies: List=None
    :return: (str, Dict)
    """
    url = f'https://graph.facebook.com/me/accounts'
    headers = {
        'Authorization': f'Bearer {user_access_token}'
    }
    # Преобразование куки в формат, используемый requests
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    response = requests.get(url, headers=headers, cookies=cookies_dict, proxies=proxies, timeout=30)

    return response.status_code, response.json()


def get_all_posts(token: str, cookies: Dict, proxies: List = None) -> (str, Dict) or str:
    """
    Получение всех постов со страницы
    :param token: str
    :param cookies: Dict
    :param proxies: List = None
    :return: (str, Dict)
    """
    url = f'https://graph.facebook.com/v20.0/me/posts'

    status_code, response = get_page_access_token(token, cookies, proxies)
    if status_code == 200:
        page_access_token = response['data'][0]['access_token']
        headers = {
            'Authorization': f'Bearer {page_access_token}',
        }
        # Преобразование куки в формат, используемый requests
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        response = requests.get(url, headers=headers, cookies=cookies_dict, proxies=proxies, timeout=30)
        return response.status_code, response.json()
    return f"Cannot get all posts: {response}"


def get_advertising_campaign(token: str, cookies: Dict, proxies: List = None) -> (str, Dict) or str:
    """
    Получение всех рекламных кампаний, которые закреплены за пользователем по токену
    :param token: str
    :param cookies: Dict
    :param proxies: List = None
    :return: (str, Dict) or str
    """
    url = f'https://graph.facebook.com/v20.0/me/personal_ad_accounts'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    # Преобразование куки в формат, используемый requests
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    response = requests.get(url, headers=headers, cookies=cookies_dict, proxies=proxies, timeout=30).json()['data']

    result = {'data': []}
    for dict in response:
        id = dict['id']
        campaign_url = f'https://graph.facebook.com/v20.0/{id}/campaigns'
        campaign_response = \
        requests.get(campaign_url, headers=headers, cookies=cookies_dict, proxies=proxies, timeout=30).json()['data']
        for campaign in campaign_response:
            result['data'].append(campaign)

    return result


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
