from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from datetime import datetime
import os
import requests
import re
import json
from keywords import keywordFunc, Sections
ts = Translator()

# connect into website
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

driver.get(
    # "https://www.livecareer.co.uk/cv-search/r/solutions-engineer-senior-pre-sales-consultant-7e6bc0a669014176959f00791e69152f")
    "file:///home/qoyyima/Downloads/WAREHOUSE%20OPERATIVE%20CV%20Example%20PARCELFORCE%20WORLDWIDE%20-%20Nechells,%20Birmingham.html")

# get raw data
content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

documentHTML = soup.find_all('div', id="document")[0]
document = documentHTML.get_text(strip=False)

scoreTemp = soup.find_all(
    'h3', class_="resume-score")[0].get_text(strip=False)
score = int(re.findall(r'\d+', scoreTemp)[0])

title = soup.find_all('h1', class_="h1")[0].get_text(strip=False)

# processing section titles
children = documentHTML.findChildren("div", recursive=False)
sections = ["title"]
sectionsId = ["title"]
sectionsContent = []
sectionsContentId = []
documentBahasa = ""
for index in range(len(children)):
    if index == 0:
        content = list(
            filter(bool, children[index].get_text(strip=False).splitlines()))
        sectionsContent.append(content)
        # contentId1 = ts.translate(
        #     children[index].get_text(strip=False), dest="id").text
        # sectionsContentId.append(list(filter(bool, contentId1.splitlines())))
        # documentBahasa += "".join(contentId1) + "\n"
    else:
        grandChildren = children[index].findChildren("div", recursive=False)
        sections.append(grandChildren[0].getText().replace("\n", ""))
        sectionsId.append(
            (grandChildren[0].getText().replace("\n", "")))
        text = []
        for index2 in range(len(grandChildren)):
            if index2 > 0:
                text.extend(
                    list(filter(bool, grandChildren[index2].get_text(strip=False).splitlines())))

        sectionsContent.append(text)
        # contentId2 = ts.translate("\n".join(text), dest="id").text
        # sectionsContentId.append(list(filter(bool, contentId2.splitlines())))
        # documentBahasa += "".join(contentId2) + "\n"

# processing data per section
keywords_data = keywordFunc()

sectionCategory = []
sectionCategoryId = []
for section in sections:
    found = False
    for attr in keywords_data:
        for value in keywords_data[attr]:
            if section.upper() == value:
                found = True
                sectionCategory.append(attr)
                sectionCategoryId.append(attr[:-2]+"id")
                break
        if found == True:
            break
    if found == False:
        sectionCategory.append("section_extra_en")
        sectionCategoryId.append("section_extra_id")

# MAPPING DATA PER SECTION

sectionsObject = Sections()

for index in range(len(sectionCategory)):
    for attr, value in sectionsObject.__dict__.items():
        if sectionCategory[index] == attr:
            newValue = value
            # newValue.extend(value+"\n"+sectionsContent[index])
            newValue.extend(sectionsContent[index])
            setattr(sectionsObject, attr, newValue)

# for index in range(len(sectionCategoryId)):
#     for attr, value in sectionsObject.__dict__.items():
#         if sectionCategoryId[index] == attr:
#             newValue = value
#             # newValue = value+"\n"+sectionsContentId[index]
#             newValue.extend(sectionsContentId[index])
#             setattr(sectionsObject, attr, newValue)

# create folder
folder_name = datetime.now().strftime(
    "%H:%M:%S--%d-%b-%Y" + "--" + title)

os.mkdir("../cv-data/"+folder_name)

# save files
fileENhtml = open("../cv-data/"+folder_name+"/index.html", "w+")
fileENhtml.write('\n'.join(content))
fileENhtml.close()

fileEN = open("../cv-data/"+folder_name+"/en.txt", "w+")
fileEN.write(document)
fileEN.close()

fileID = open("../cv-data/"+folder_name+"/id.txt", "w+")
fileID.write(documentBahasa)
fileID.close()

fileScore = open("../cv-data/"+folder_name+"/score.txt", "w+")
fileScore.write(str(score))
fileScore.close()

with open("../cv-data/"+folder_name+"/sections.json", "w+") as fileSections:
    data = {}
    data["sections"] = sections
    data["sectionsId"] = sectionsId
    data["contents"] = sectionsContent
    data["contentsId"] = sectionsContentId
    json.dump(data, fileSections)
fileSections.close()

driver.close()

# print(sectionsObject.__dict__)
print(sectionsObject.__dict__,
      "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# send data to server
r = requests.post('http://localhost:8080/insert/cv',
                  json={"Folder": folder_name, "Title": title, "HTML": "", "En": document, "Id": documentBahasa, "Score": score, "Sections": sections, "SectionCategory": sectionCategory, "SectionsId": sectionsId, "SectionCategoryId": sectionCategoryId, "SectionsContent": sectionsObject.__dict__, "ListSectionsContent": sectionsContent, "ListSectionsContentId": sectionsContentId})
print(r, "successfully send data")


# Full HTML Page Source
def getFullHTMLPageSource():
    file = open("index.html", "w")
    file.write(content)
    file.close()
