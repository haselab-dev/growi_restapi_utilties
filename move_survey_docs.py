import pprint
import numpy as np
from utils import get_page_list_by_page, create_page

base_url = 'https://<domain>'
api_token = 'api_token'
users = [...]

for user in users:
    print(f'[{user}]')
    q = f'/user/{user}/survey'
    page_list = get_page_list_by_page(base_url, api_token, q)
    for page in page_list:
        path = page['path']
        name = path.split('/')[-1]
        new_path = f'/survey/{name}'
        if name == ['__template', '_template', 'survey'] : continue
        print(f'{path} -> {new_path}')
        # pprint.pprint(page)
    print('='*100)