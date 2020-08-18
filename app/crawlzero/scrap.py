import os
#import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options


class Scraper(object):
    #def __init__(self):
        #self.path = path

    def price_match(self, s):
        value = re.search(r'[0-9].*[0-9]', s)
        x = value.group(0).lstrip()
        return re.sub(',', "", x)

    def extract(self, link):
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

            return self.price_match(s)


    def parser(self, file):
        infile = pd.read_excel(file)
        
        infile["Validity"] = ""

        for i in range(len(infile['link'])):
            actual = self.price_match(str(infile['price'][i]))
            predicted = self.extract(str(infile['link'][i]))
            #result(actual,predicted, i)
            if(actual == predicted):
                infile['Validity'][i] = "Valid"
            else:
                infile['Validity'][i] = "InValid" + predicted


        #pathing = os.path.join(infile)
        outfile = infile.to_csv()
        return outfile
        #os.remove(pathing)