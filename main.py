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
    today_strftime = "_01_30_2023.json"
    for key in xml_keys():
        if key.endswith(today_strftime):
            return key
    return False
def todays_transactions_indexes():
    key = is_today_available()
    if key:
        indexes = []
        js_url = urllib.parse.urljoin(urls.get('data_base'),key)
        js = fetch(js_url).json()
        data = pd.DataFrame(js)
        for name in config.reps_to_follow:
            last_name = name.split('|')[1].strip()
            first_name = name.split('|')[0].strip()
            transaction_types = name.split('|')[-1].strip()
            

            # if transaction_types.strip().lower() == 'a':
            #     t = 'All'
            # elif transaction_types.strip().lower() == 'b':
            #     t = 'purchase'
            # elif transaction_types.strip().lower() == 's':
            #     t = 'SELL'
            # r = data.index[data['last_name'] == last_name.lower().capitalize()].tolist()
            # for i in r:
            #     if data.iloc[i]['first_name'] == first_name and data.iloc[i]['type'] == :
            #         indexes.append(r)
        # RETURN A LIST THAT HAS A LIST OF TRANSACTIONS FOR EACH FOLLOWED REP.
        return indexes
def process_transactions():
    transaction_indexes = todays_transactions_indexes()
    for rep in





