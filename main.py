import requests
import json
import time
import pandas as pd
from requests.adapters import HTTPAdapter

url_search = 'http://139.162.55.71/search/'
url_re = 'http://139.162.55.71/related_components/'

keys = ['大黄', '茯苓', '当归']
table_names = ['TCM_symptom', 'Mol', 'Gene', 'Disease', 'Syndrome', 'MM_symptom']

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))

for key in keys:
    # 检索部分
    search_data = {'table_name':'Herb', 'key':key}
    try:
        search = s.post(url_search, data=search_data)
    except:
        print('{} failed'.format(key))
        continue
    rrid = json.loads(search.text)['data'][0]['Herb_id']
    r = {}
    print(rrid)
    # 爬取表格部分
    for table_name in table_names:
        try:
            r_data = {'rrid':rrid, 'table_name':table_name, 'filter':'0'}
            r[table_name] = s.post(url_re, data=r_data, timeout=15)
            print('{} {} done'.format(key, table_name))
            time.sleep(3)
    # 处理部分
            data = json.loads(r[table_name].text)['data']
            D = pd.DataFrame()
            for i in range(len(data)):
                temp = pd.DataFrame.from_dict(data[i], orient='index').T
                D = pd.concat((D, temp))
            D.to_csv(r'./资料/{}+{}.csv'.format(key, table_name), encoding='gb18030', index=False)
        except:
            print('{} {} failed'.format(key, table_name))