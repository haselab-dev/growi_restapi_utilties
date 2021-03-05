# For Growi v4.2.10

import json
import requests
from typing import Union


# Growi Rest API向けのError
class GrowiAPIError(Exception):
    def __init__(self, description):
        super().__init__()
        self.description = description
    
    def __repr__(self):
        return str(self.description)

    def __str__(self):
        return str(self.description)


##### Get Information #####

# 正常に動作することを確認できていない
def exist_page(base_url: str, api_token: str, page_path: str) -> bool:
    """
    [Experiment] check existance of the spcified page
    """
    res = get_page_info(base_url, api_token, page_path)

    if res.status_code == 200:
        return json.loads(res.text)['ok']
    else:
        raise GrowiAPIError(res.text)


def get_page_info(base_url: str, api_token: str, page_path: str) -> dict:
    """
    get page information
    """
    req_url = '{}{}'.format(base_url, '/_api/pages.get')
    params={'access_token': f'{api_token}', 'path': page_path}
    res = requests.get(req_url, params=params)

    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)


def get_page_list_by_page(base_url: str, api_token: str, page_path: str, limit:Union[int, None]=None) -> dict:
    """
    get page list under the specified page path
    """
    req_url = '{}{}'.format(base_url, '/_api/pages.list')
    limit = 1e10 if limit is None else limit
    queries = {
        'access_token': f'{api_token}',
        'path': page_path,
        'limit': limit,
    }
    res = requests.get(req_url, params=queries)
    if res.status_code == 200:
        return json.loads(res.text)['pages']
    else:
        raise GrowiAPIError(res.text)


def get_page_list_by_user(base_url: str, api_token: str, user: str, limit:Union[int, None]=None) -> dict:
    """
    get page list owned by specified user
    """
    req_url = '{}{}'.format(base_url, '/_api/pages.list')
    limit = 1e10 if limit is None else limit
    queries = {
        'access_token': f'{api_token}',
        'user': user,
        'limit': limit,
    }
    res = requests.get(req_url, params=queries)
    if res.status_code == 200:
        return json.loads(res.text)['pages']
    else:
        raise GrowiAPIError(res.text)


##### Create Page #####

def create_page(base_url: str, api_token: str, page_path: str, body: str, grant: int=1) -> dict:
    """
    create page
    """
    req_url = '{}{}'.format(base_url, '/_api/v3/pages')
    params = {
        'access_token': f'{api_token}',
    }

    payloads = {
        'path': page_path,
        'body': body,
        'grant': grant,
    }

    res = requests.post(req_url, data=payloads, params=params)
    if res.status_code == 201:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)


def update_page(base_url: str, api_token: str, page_path: str, body: str, grant: int=1) -> dict:
    """
    update page
    """
    res = get_page_info(base_url, api_token, page_path)
    success = res['ok']
    if not success:     # ページの存在しない場合get_page_infoはstatus_code=200で失敗する
        raise GrowiAPIError(res)
    page_info = res['page']
    page_id = page_info['_id']
    revision_id = page_info['revision']['_id']

    req_url = '{}{}'.format(base_url, '/_api/pages.update')
    params = {
        'access_token': f'{api_token}',
    }

    payloads = {
        'path': page_path,
        'body': body,
        'page_id': str(page_id),
        'revision_id': str(revision_id),
        'grant': grant,
    }

    res = requests.post(req_url, data=payloads, params=params)
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)


#### Delete Page #####

# ページの削除はRestAPIではできない模様
# 厳密にはログイン状態を維持した状態でRest APIを叩かないと削除できない(Seleniumやbeautifusoupを駆使すれば削除は可能)
"""
def delete_page(base_url: str, api_token: str, page_path: str, recursively: bool=True, completely: bool=True) -> dict:
    page_info = get_page_info(base_url, api_token, page_path)
    page_id = page_info['_id']
    revision_id = page_info['revision']['_id']

    req_url = '{}{}'.format(base_url, '/_api/pages.remove')
    params = {
        'access_token': f'{api_token}',
    }

    payloads = {
        'page_id': str(page_id),
        'revision_id': str(revision_id),
        'recursively': recursively,
        'completely': completely,
    }

    res = requests.post(req_url, data=payloads, params=params)
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)
"""


##### Rename Page #####

def rename_page(base_url: str, api_token: str, src_page_path: str, target_page_path: str, is_remain_meta_data: bool=True) -> dict:
    """
    rename page (change page path)
    """
    res = get_page_info(base_url, api_token, src_page_path)
    success = res['ok']
    if not success:     # ページの存在しない場合get_page_infoはstatus_code=200で失敗する
        raise GrowiAPIError(res)
    page_info = res['page']
    page_id = page_info['_id']
    revision_id = page_info['revision']['_id']

    req_url = '{}{}'.format(base_url, '/_api/v3/pages/rename')
    params = {
        'access_token': f'{api_token}',
    }

    # all queries required
    payloads = {
        'pageId': page_id,
        'revisionId': revision_id,
        'path': src_page_path,
        'newPagePath': target_page_path,
        'isRemainMetadata': 'true' if is_remain_meta_data else 'false',
    }

    res = requests.put(req_url, data=payloads, params=params)
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise GrowiAPIError(res.text)


##### Get Tag #####

def get_tag_list(base_url: str, api_token: str) -> dict:
    """
    get tag list
    """
    req_url = '{}{}'.format(base_url, '/_api/tags.list')
    params = {
        'access_token': f'{api_token}',
    }

    res = requests.get(req_url, params=params)
    if res.status_code == 200:
        return json.loads(res.text)['data']
    else:
        raise GrowiAPIError(res.text)

def get_tags_by_page(base_url: str, api_token: str, page_path: str) -> list:
    """
    get tags annotated on specified pate
    """
    res = get_page_info(base_url, api_token, page_path)
    success = res['ok']
    if not success:     # ページの存在しない場合get_page_infoはstatus_code=200で失敗する
        raise GrowiAPIError(res)
    page_id = res['page']['_id']

    req_url = '{}{}'.format(base_url, '/_api/pages.getPageTag')
    params = {
        'access_token': f'{api_token}',
        'pageId': page_id
    }

    res = requests.get(req_url, params=params)
    if res.status_code == 200:
        return json.loads(res.text)['tags']
    else:
        raise GrowiAPIError(res.text)
