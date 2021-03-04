import pprint
from utils import *

if __name__ == '__main__':
    base_url = 'https://<wiki domain>'
    api_token = 'API Token'

    body = '# Test\nThis page is created automatically.'
    res = create_page(base_url, api_token, '/test/hase', body)
    pprint.pprint(res)

    body = '# Test\nThis page is created automatically.\nThis page is created automatically.\nThis page is created automatically.'
    res = update_page(base_url, api_token, '/test/hase', body)
    pprint.pprint(res)

    res = rename_page(base_url, api_token, '/test/hase2', '/test/hase')
    pprint.pprint(res)

    res = get_page_info(base_url, api_token, '/test/hase')
    pprint.pprint(res)
