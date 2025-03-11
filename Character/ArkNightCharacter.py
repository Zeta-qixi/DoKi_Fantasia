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

voice_filter = [
 '任命助理',
 '交谈1',
 '交谈2',
 '交谈3',
 '晋升后交谈1',
 '晋升后交谈2',
 '信赖提升后交谈1',
 '信赖提升后交谈2',
 '信赖提升后交谈3',
 '闲置',
 '干员报到',
 '观看作战记录',
 '精英化晋升1',
 '精英化晋升2',
 '编入队伍',
 '任命队长',
 '行动出发',
 '行动开始',
 '选中干员1',
 '选中干员2',
 '部署1',
 '部署2',
 #'作战中1',
 #'作战中2',
 #'作战中3',
 #'作战中4',
 '完成高难行动',
 '3星结束行动',
 '非3星结束行动',
 '行动失败',
 '进驻设施',
 #'戳一下',
 '信赖触摸',
 '问候',
 '新年祝福',
 '周年庆典']
        

class Character_Story:
    
    def init_for_wiki(self):
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
            k= v['data-title'].strip()
            voice_data[k] = v.find('div').text
        return cls(voice_data)

    def get_voice_info(self):
        
        return voice_template.format('\n'.join([f"- [{k}]：{v}" for k,v in self.voice.items() if k in voice_filter]))
    
    
class Character:
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
    
    def __init__(self, name, gender, experience, origin_place, birthday, race, height, infection_status, archive, voice):
        self.name = name
        self.gender = gender
        self.experience = experience
        self.origin_place = origin_place
        self.birthday = birthday
        self.race = race
        self.height = height
        self.infection_status = infection_status
        self.archive = archive # 档案
        self.voice = voice
        

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
    
            
        result['voice'] = Character_Voice.init_for_wiki(soup)
        return cls(**result)

    def get_base_info(self):
        return base_template.format(self.name, self.gender)
    
    def get_archive_info(self):
        num = ['一', '二', '三', '四', '五']
        text = '\n'.join([f'- 剧情{num[i]}：{t}' for i, t in enumerate(self.archive)])
        return f"## 角色剧情\n{text}\n"
            
    
    def get_full_info(self) -> str:
        base_info = self.get_base_info()
        archive_info = self.get_archive_info()
        voice_info = self.voice.get_voice_info()
        
        full_info = f"{base_info}\n{archive_info}\n{voice_info}"
        return full_info
    

    




