from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import json
import time
import pandas as pd
import requests

def get_driver_instance():
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
    return driver

def get_page(driver, url):
    driver.get(url)
    title = driver.title
    driver.implicitly_wait(1.0)
    s = BeautifulSoup(driver.page_source, 'lxml')
    return s

def get_cats(s):
    c = s.find_all(class_="menu-hsbroad-wrapper")[0]
    cc = c.select("ul>li>a")
    cats = []
    for x in cc:
        id_ = x.get("id")
        title = x.get("title")

        if title and id_ and id_.startswith("menu_boards2"):            
            cats.append((title, id_))
    return cats

def get_one_cat_items(tds):
    
    href = tds[0].select("a")[0].get("href")
    name = tds[0].select("a")[0].get_text()
    company_number = tds[1].get_text()
    avg_price = tds[2].select("span")[0].get_text()
    diff_value = tds[3].select("span")[0].get_text()
    diff_percent = tds[4].select("span")[0].get_text()
    volume_batch = tds[5].get_text()
    volume_value = tds[6].get_text()

    leader_name = tds[7].select("a")[0].get_text()
    leader_symbol = tds[7].get_text()
    m = re.match("^.*\((.*)\)$", leader_symbol)
    leader_symbol = m.group(1)

    leader_diff_value = tds[8].select("span")[0].get_text()
    leader_current_price = tds[9].select("span")[0].get_text()
    leader_diff_ratio = tds[10].select("span")[0].get_text()
    
    r = (name, company_number, avg_price, diff_value, diff_percent, volume_batch, volume_batch, leader_name, leader_symbol, leader_diff_ratio, leader_current_price, leader_diff_value)
    return r

def format_url(cat):
    id_ = cat[1].split("-")[-1]
    url = 'https://18.push2his.eastmoney.com/api/qt/stock/kline/get?secid=%s&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&beg=0&end=20500101&smplmt=460&lmt=1000000' % id_
    return url

def get_one_cat(cat):
    time.sleep(0.2)
    url = format_url(cat)
    res = requests.get(url)
    return json.loads(res.text).get("data").get("klines")
    

if __name__ == "__main__":
    east = "http://quote.eastmoney.com/center/hsbk.html"
    driver = get_driver_instance()
    s = get_page(driver, east)
    cats = get_cats(s)
    print(cats)
    
    for cat in cats:
        klines = get_one_cat(cat)
        print(klines)
        klines = list(map(lambda x: x.split(","), klines))
        print(klines)
        cols = ["time", "open", "close", "high", "low", "volume_units", "volume_value", "range", "diff_ratio", "diff_value", "exchange_ratio"]
        dataframe = pd.DataFrame(columns=cols, data=klines)
        print(dataframe)
        print(cat)
        name = cat[0].replace("/", "-")
        dataframe.to_csv(name + ".csv")
    driver.quit()
        

