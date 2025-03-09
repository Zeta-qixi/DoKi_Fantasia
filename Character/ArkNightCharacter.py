import re
from typing import Dict, List
from bs4 import BeautifulSoup

base_template =  """
## 基本信息
- 作品：明日方舟
- 角色名称：{}
- 性别：{}
- 对用户称呼：博士
"""


voice_template ="""
## 语音
{}
"""
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
        self.archive = archive # 档案
        self.voice = ''
        
    def add_voice(self, v):
        self.voice = v
    
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
        
        for _i, text in enumerate(raw_texts):
            if '【代号' in text: break
        base_info = raw_texts[_i].strip()
        pattern = r'【(.*?)】(.*?)(?=【|$)'
        matches = re.findall(pattern, base_info, flags=re.DOTALL)
        result = {}
        for key, value in matches:
            attr_key = cls.params.get(key)
            if attr_key is not None:
                cleaned_value = value.strip()
                result[attr_key] = cleaned_value
        
        result['archive'] = []
        for i, text in enumerate(raw_texts):
            if '档案资料' in text:
                result['archive'].append(raw_texts[i+1].strip())
   
            
        
        return cls(**result)

    def get_base_info(self):
        return base_template.format(self.name, self.gender)
    
    def get_archive_info(self):
        num = ['一', '二', '三', '四', '五']
        text = '\n'.join([f'- 剧情{num[i]}：{t}' for i, t in enumerate(self.archive)])
        return f"\n{text}\n"
            
    
    
class Character_Story:
    ...

class Character_Voice:
    
    def __init__(self, data: Dict[str, str]):
        self.voice = data
    
    @classmethod
    def init_for_wiki(cls, soup: BeautifulSoup):
        voice_soup = soup.find('div',{'data-toc-title':'语音记录'})
        voice_soup.find_all('div',{'class':'voice-data-item'})[0]['data-title']
        voice_data = {}
        for v in voice_soup.find_all('div',{'class':'voice-data-item'}):
            
            if (k:= v['data-title'].strip()) not in ['标题']:
                voice_data[k] = v.find('div').text
            
        return cls(voice_data)

    def get_voice_info(self):
        
        return voice_template.format('\n'.join([f"- [{k}]：{v}" for k,v in self.voice.items()]))
    

class Character(Character_Info, Character_Story, Character_Voice):
    def __init__(self):
        ...
    