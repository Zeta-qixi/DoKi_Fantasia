import re
from typing import Dict, List
from bs4 import BeautifulSoup

class Character_Info:
    # 根据属性名设计的参数列表
    params = {
    '代号': 'name',
    '性别': 'gender',
    '战斗经验': 'experience',
    '出身地': 'origin_place',
    '生日': 'birthday',
    '种族': 'race',
    '身高': 'height',
    '矿石病感染情况': 'infection_status'
    }
    
    def __init__(self, name, gender, experience, origin_place, birthday, race, height, infection_status, archive):
        self.name = name
        self.gender = gender
        self.experience = experience
        self.origin_place = origin_place
        self.birthday = birthday
        self.race = race
        self.height = height
        self.infection_status = infection_status
        self.archive = archive # 档案 1 - 4 + 晋升记录
    
    @classmethod
    def init_for_wiki(cls, soup: BeautifulSoup):
        
        sub_soup = soup.find_all('table', {'class': 'wikitable', 
                        'class': 'mw-collapsible',
                        'class': 'mw-made-collapsible',
                        'class': 'logo'}) 
        profile = [i for i in sub_soup if '人员档案' in i.text]
        assert len(profile) == 1
        profile = profile[0]

        raw_texts = []
        for div in soup.find_all('div', {'class': "poem"}):
            raw_texts.append(div.text)
            
        base_info = raw_texts[6].strip()
        pattern = r'【(.*?)】(.*?)(?=【|$)'
        matches = re.findall(pattern, base_info, flags=re.DOTALL)
        result = {}
        for key, value in matches:
            attr_key = cls.params.get(key)
            if attr_key is not None:
                cleaned_value = value.strip()
                result[attr_key] = cleaned_value
        
        result['archive'] = []
        for i in range(14,24,2):
            result['archive'].append(raw_texts[i].strip())
        
        return cls(**result)
    

    
class Character_Voice:
    ...

class Character_Story:
    
    def __init__(self, data: List[Dict[str, str]]):
        self.voice = data
    
    @classmethod
    def init_for_wiki(cls, soup: BeautifulSoup):
        voice_soup = soup.find('div',{'data-toc-title':'语音记录'})
        voice_soup.find_all('div',{'class':'voice-data-item'})[0]['data-title']
        voice_data = []
        for v in voice_soup.find_all('div',{'class':'voice-data-item'}):
            voice_data.append(
                {v['data-title'].strip(): v.find('div').text}
            )
        
        return cls(voice_data)
    

class Character(Character_Info, Character_Story, Character_Voice):
    def __init__(self):
        ...
    