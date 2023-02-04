import datetime
import urllib.parse
import httpx
import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path
import pandas as pd
import json
import config

database_file = Path('trade_info.db')
urls = {
    'xmlEP':'https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/filemap.xml',
    'data_base':'https://house-stock-watcher-data.s3-us-west-2.amazonaws.com',
}
class representative():
    def __init__(self,rep):
        self.first_name = rep.split('|')[0].strip()
        self.last_name = rep.split('|')[1].strip()
        self.transactions_types = rep.split('|')[-1].lower().strip()
        self.transactions = []
def fetch(location):
    headers = {}
    with httpx.Client(headers=headers,http2=True) as c:
        soup = c.get(location)
    return soup
def xml_keys():
    root = ET.fromstring(fetch(urls.get('xmlEP')).text)
    for child in root:
        for key in child:
            yield key.text
def is_today_available():
    today_date_object = datetime.date.today()
    today_strftime = today_date_object.strftime("_%m_%d_%Y.json")
    today_strftime = "_12_22_2022.json"
    for key in xml_keys():
        if key.endswith(today_strftime):
            return key
    return False
def load_json_into_data_frame():
    key = is_today_available()
    if key:
        js_url = urllib.parse.urljoin(urls.get('data_base'),key)
        js = fetch(js_url).json()
        data = pd.DataFrame(js)
        return data
def build_reps():
    reps = []
    data = load_json_into_data_frame()
    print(data.to_string())
    for r in config.reps_to_follow:
        rep = representative(r)
        reps.append(rep)
        d = data.index[data['last_name'] == rep.last_name].tolist()
        for x in d:
           if data.iloc[x]['first_name'] == rep.first_name:
               transactions = data.iloc[x]['transactions']
               for t in transactions:
                   rep.transactions.append(t)
    return reps

reps = build_reps()
for rep in reps:
    for t in rep.transactions:
        print(t.get('ticker'),t.get('transaction_type'))