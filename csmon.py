import subprocess

import re
import sys
import trafilatura
import requests
from bs4 import BeautifulSoup as bs
URL = "https://www.csmonitor.com//World/Middle-East/2023/0519/Turkish-opposition-clings-to-election-hopes-against-the-odds"

def get_content_new(URL):
    headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    html = requests.get(URL, headers=headersparam).content  
    # print(html)
    data = bs(html, 'lxml')
    # print(data)
    with open("tmp.html", "w",encoding="utf-8") as file:
        # Write the text to the file
        file.write(str(data))
    # mm = trafilatura.extract(str(data),target_lang='en',date_extraction_params={"extensive_search": True}, include_tables = True, output_format = "xml")
    # mm = bs(mm, 'lxml')
    # print(mm)
    # print("#"*230)
    articles = data.find_all('div', {'class': 'small-centered small-12 columns'})
    story_two = articles[0].find_all('div', {'class': 'story-two eza-body small-11 small-centered medium-10 large-12 deep-read story-body-toggle-content prem default truncate-for-paywall'})
    story_two = bs(str(story_two[0]), 'lxml')
    with open("tmp2.html", "w",encoding="utf-8") as file:
        # Write the text to the file
        file.write(str(story_two))
    # print(mm)  
    # print("#"*230)

    story_two = trafilatura.extract(str(story_two),target_lang='en',date_extraction_params={"extensive_search": True}, include_tables = True, output_format = "xml")
                                
    story_two = bs(story_two, 'lxml')
    story_two = story_two.get_text()
    return story_two



# URL = 'https://draxe.com/recipes/dairy-free-eggnog-recipe/'


content = get_content_new(URL)
print(content)