import os
#import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from .mailing import mail,mailfail
from myproject.celery_app import app as celery_app
from celery import Task
from django.core.files.storage import default_storage

def price_match(s):
    value = re.search(r'[0-9].*[0-9]', s)
    x = value.group(0).lstrip()
    return re.sub(',', "", x)

def extract(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disable-dev-shm-usage')        
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome(executable_path = binary_path,options=chrome_options)
    #driver.implicitly_wait(20)


    driver.get(link)
    html = driver.execute_script("return document.documentElement.innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    
    price_text = ""
    s=""
    #price = soup.findAll(['p', 'div', 'span'], {re.compile(r'(.*?pric.*?)', re.IGNORECASE)} )
    def is_price(tag):
        for k, v in tag.attrs.items():
            if 'pric' in v:
                return True
            elif isinstance(v, list) and any('pric' in i for i in v):
                return True
    
    tags = soup.find_all(is_price)
    if tags:
        for tag in tags:
            price_text = price_text + tag.get_text()+'\n'

    if not price_text:
        driver.close()
        return "Error"
        
    else:
        for i in price_text.split(" "):
            s = s+i+"\n"
        driver.close()

        return price_match(s)

@celery_app.task
def scrapmail(file, receiveraddr):
    try:
        with open(default_storage.open(file), 'r') as f:
            infile = pd.read_excel(f)
        
        infile["Validity"] = ""

        for i in range(len(infile['link'])):
            actual = price_match(str(infile['price'][i]))
            predicted = extract(str(infile['link'][i]))
            #result(actual,predicted, i)
            if(actual == predicted):
                infile['Validity'][i] = "Valid"
            else:
                infile['Validity'][i] = "InValid" + predicted


        #pathing = os.path.join(infile)
        outfile = infile.to_csv()
        mail(receiveraddr, outfile)
    # return outfile
    #os.remove(pathing)
    except Exception as e:
        mailfail(receiveraddr, str(e))


# def scrapmail(receiveraddr):
#     mailfail("rajagadamsetty@gmail.com", "t5esting cle")