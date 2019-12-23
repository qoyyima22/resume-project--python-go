from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from datetime import datetime
import os
import requests
import re

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")

driver.get(
    "https://www.livecareer.co.uk/cv-search/r/warehouse-operative-eaa2942db7b2467bb9c4f9869d62b608")

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

documentHTML = soup.find_all('div', id="document")[0]
document = documentHTML.get_text()
scoreTemp = soup.find_all('h3', class_="resume-score")[0].get_text()
score = int(re.findall(r'\d+', scoreTemp)[0])
title = soup.find_all('h1', class_="h1")[0].get_text()

ts = Translator()

documentbahasa = ts.translate(document, dest="id").text

folder_name = datetime.now().strftime(
    "%H:%M:%S--%d-%b-%Y" + "--" + title)

os.mkdir("../cv-data/"+folder_name)

fileENhtml = open("../cv-data/"+folder_name+"/index.html", "w+")
fileENhtml.write(content)
fileENhtml.close()

fileEN = open("../cv-data/"+folder_name+"/en.txt", "w+")
fileEN.write(document)
fileEN.close()

fileID = open("../cv-data/"+folder_name+"/id.txt", "w+")
fileID.write(documentbahasa)
fileID.close()

fileScore = open("../cv-data/"+folder_name+"/score.txt", "w+")
fileScore.write(str(score))
fileScore.close()

driver.close()

r = requests.post('http://localhost:8080/insert/cv',
                  json={"Folder": folder_name, "Title": title, "HTML": "", "En": document, "Id": documentbahasa, "Score": score})
print(r, "successfully send data")

# Full HTML Page Source

# file = open("index.html", "w")
# file.write(content)
# file.close()
