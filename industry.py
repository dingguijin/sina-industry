from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_driver_instance():
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
    return driver


def get_page(driver, url):
    driver.get(url)
    title = driver.title
    driver.implicitly_wait(1.0)
    s = BeautifulSoup(driver.page_source, 'lxml')
    return s

def get_cat(s):
    c = s.find(id="industrynav")
    c = c.find_all("li")
    x = list(map(lambda x: x.select("li > a")[0].get_text(), c))
    y = list(map(lambda x: x.get("id"), c))    
    return list(zip(x, y))

def get_one_cat_items(tds):
    href = tds[0].select("a")[0].get("href")
    name = tds[0].select("a")[0].get_text()
    company_number = tds[1].get_text()
    avg_price = tds[2].select("span")[0].get_text()
    diff_value = tds[3].select("span")[0].get_text()
    diff_percent = tds[4].select("span")[0].get_text()
    volume_batch = tds[5].get_text()
    volume_value = tds[6].get_text()

    r = (name, href, company_number, avg_price, diff_value, diff_percent, volume_batch, volume_batch)
    return r

def get_one_cat(driver, cat):
    one_cat = driver.find_element(By.CSS_SELECTOR, "#" + cat[1])
    if not one_cat:
        return
    driver.implicitly_wait(10.0)
    time.sleep(1.0)
    one_cat.click()
    time.sleep(1.0)
    driver.implicitly_wait(10.0)
    s = BeautifulSoup(driver.page_source, 'lxml')
    s = s.find_all("div", class_="tblOuter")
    s = s[0].select("tbody>tr")
    items = []
    for i in s:
        d = i.find_all("td")
        items.append(get_one_cat_items(d))
    return items
    

if __name__ == "__main__":
    driver = get_driver_instance()
    s = get_page(driver, "http://finance.sina.com.cn/stock/sl")
    cats = get_cat(s)
    for cat in cats:
        print(cat)
        items = get_one_cat(driver, cat)
        print(len(items))
        cols = ["name", "link", "companys", "avg_price", "diff_price", "diff_ratio", "volume_units", "volume_value"]
        dataframe = pd.DataFrame(columns=cols, data=items)
        print(dataframe)
        dataframe.to_csv(cat[0] + ".csv")
    driver.quit()
        

