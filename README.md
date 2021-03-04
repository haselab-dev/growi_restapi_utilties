# growi_restapi_utilties

## What's growi_restapi_utilties?

内部処理の用途でGrowiに実装されているRestAPIをPythonから叩くためのツール．

## **Caution!!**

GrowiのRestAPIは内部処理のために用意されているAPIであるため，
今後大幅にその仕様が変更される可能性があり，
それに伴いこのツールを使用できなくなるかもしれない．

## Get started

GrowiのRestAPIを使用するには**APIトークン**を用意する必要がある．
APIトークンの取得はGrowiのアカウント設定の``API設定``から取得することができる．

### 指定したページの情報を取得

```python
import pprint
from utils import get_page_info

base_url = 'https://<wiki domain>'
api_token = 'API Token'

page_path = '/sample/page
res = get_page_info(base_url, api_token, page_path)
pprint.pprint(res)
```

### 新たにページを作成

```python
import pprint
from utils import create_page

base_url = 'https://<wiki domain>'
api_token = 'API Token'

page_path = '/sample/page
body = '# Sample\nThis page is created automatically.'
res = create_page(base_url, api_token, page_path, body)
pprint.pprint(res)
```

### ページを更新(上書き)

```python
import pprint
from utils import update_page

base_url = 'https://<wiki domain>'
api_token = 'API Token'

page_path = '/sample/page
body = '# Sample(updated)\nSample Sample Sample'
res = update_page(base_url, api_token, page_path, body)
pprint.pprint(res)
```

### ページ名を変更(ページを移動)

```python
import pprint
from utils import rename_page

base_url = 'https://<wiki domain>'
api_token = 'API Token'

src_page_path = '/sample/page
target_page_path = '/test/page
res = rename_page(base_url, api_token, src_page_path, target_page_path)
pprint.pprint(res)
```
