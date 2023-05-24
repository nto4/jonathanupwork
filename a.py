import trafilatura
import sys
from bs4 import BeautifulSoup as bs
import re
import requests

URL = "https://www.csmonitor.com/World/Middle-East/2023/0519/Turkish-opposition-clings-to-election-hopes-against-the-odds"

def get_quickread(URL):
    headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    html = requests.get(URL, headers=headersparam).content  
    data = bs(html, 'html.parser')
    articles = data.find_all('div', {'class': 'small-centered small-12 columns'})
    story_one = articles[0].find_all('div', {'class': 'story-one eza-body small-11 small-centered medium-10 large-12 quick-read story-body-toggle-content prem truncate-for-paywall'})
    story_one = trafilatura.extract(str(story_one[0]),target_lang='en',date_extraction_params={"extensive_search": True}, include_tables = True, output_format = "xml")
    story_one = bs(story_one, 'lxml')
    story_one = story_one.get_text()
    return story_one



def get_deepread(URL):
    headersparam = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    html = requests.get(URL, headers=headersparam).content  
    data = bs(html, 'html.parser')
    articles = data.find_all('div', {'class': 'small-centered small-12 columns'})
    story_two = articles[0].find_all('div', {'class': 'story-two eza-body small-11 small-centered medium-10 large-12 deep-read story-body-toggle-content prem default truncate-for-paywall'})
    story_two = trafilatura.extract(str(story_two[0]),target_lang='en',date_extraction_params={"extensive_search": True}, include_tables = True, output_format = "xml")
    story_two = bs(story_two, 'lxml')
    story_two = story_two.get_text()
    return story_two

URL = "https://www.csmonitor.com/The-Culture/2023/0518/With-new-Legend-of-Zelda-release-a-chance-to-be-a-kid-again"

print(get_deepread(URL))