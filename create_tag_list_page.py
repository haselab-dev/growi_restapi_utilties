import pprint
import numpy as np
from utils import get_tag_list, update_page
from utils import exist_page, get_page_info

base_url = 'https://<domain>'
api_token = 'api_token'
tag_list_page_path = '/path/to/tags'



item_tmpl = \
    '<div class="tag_item" style="height: 40px; border-bottom: 2px solid; border-color: gainsboro;">\n' \
    '<a href="{link}" style="color: dimgray;">\n' \
    '<p style="color: dimgray; padding-left:10px; padding-top: 9px;"># {tag_name} ({tag_count})</p>\n' \
    '</a>\n' \
    '</div>'

tag_list = np.array(get_tag_list(base_url, api_token))
tag_names = np.array([tag['name'].lower() for tag in tag_list])
indices = np.argsort(tag_names)
entity_body = []
for item in tag_list[indices]:
    tag_name = item['name']
    tag_count = item['count']
    link = base_url + '/_search?q=tag:{}'.format(tag_name)
    entity_body += [item_tmpl.format(link=link, tag_name=tag_name, tag_count=tag_count)]
description = 'wiki内の全タグを集めました．記事探しにお使いください．タグ名はリンクになっているのでクリックするとそのタグが付いている記事の一覧を見ることができます．\n\nただし，一部のタグはタグ名にスペースがあるなどの理由で記事一覧に飛ぶことができないようです．'
entity_body = '# Tags\n{}\n<br>{}'.format(description, '\n'.join(entity_body))
pprint.pprint(entity_body)

res = update_page(base_url, api_token, tag_list_page_path, entity_body, 1)
pprint.pprint(res)