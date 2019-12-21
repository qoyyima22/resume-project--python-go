from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from datetime import datetime
import os

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")

driver.get("https://www.livecareer.co.uk/cv-search/r/production-liaison-officer-48bd3cd726974e2b882369c5dd4331d4")

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

documentHTML = soup.find_all('div', id="document")[0]
document = documentHTML.get_text()
score = soup.find_all('h3', class_="resume-score")[0].get_text()
title = soup.find_all('h1', class_="h1")[0].get_text()

ts = Translator()

documentbahasa = ts.translate(document, dest="id")

folder_name = datetime.now().strftime(
    "%H:%M:%S--%d-%b-%Y" + "--" + title + ".txt")

os.mkdir("../cv-data/"+folder_name)

fileENhtml = open("../cv-data/"+folder_name+"/index.html", "w+")
fileENhtml.write(content)
fileENhtml.close()

fileEN = open("../cv-data/"+folder_name+"/en.txt", "w+")
fileEN.write(document)
fileEN.close()

fileID = open("../cv-data/"+folder_name+"/id.txt", "w+")
fileID.write(documentbahasa.text)
fileID.close()


fileScore = open("../cv-data/"+folder_name+"/score.txt", "w+")
fileScore.write(score)
fileScore.close()

driver.close()


# Full HTML Page Source

# file = open("index.html", "w")
# file.write(content)
# file.close()
