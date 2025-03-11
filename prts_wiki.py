import os
from bs4 import BeautifulSoup
from crawler.requester import requester
from Character.ArkNightCharacter import Character
import sys
import os


def func(name):

    url = f'https://prts.wiki/w/{name}'   
    html = requester.get(url)
    soup = BeautifulSoup(html, 'html.parser')
    role = Character.init_for_wiki(soup)
    
    with open('prompt/gpt语言分析.txt','r') as f:
        d = f.read()
    with open(f'Output/raw/{role.name}.txt','w') as f:
        f.write(d.format(role.get_full_info()))
        
if __name__ == "__main__":
    func('安洁莉娜')