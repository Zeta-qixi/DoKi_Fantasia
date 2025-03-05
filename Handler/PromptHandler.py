import os
from pathlib import Path

class PromptHandler:
    def __init__(self, dir='prompt'):
        
        self._prompt = {}
        self.current_prompt = None
        self.dir = Path(dir)
        
        for file_path in self.dir.iterdir():
            if file_path.suffix.lower() != '.txt':
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    name_part = lines[0].split('- Role: ', 1)
                    assert len(name_part) == 2, '错误的格式'
                    name = name_part[1].strip()
                    self._prompt[name] = ''.join(lines)
            except Exception as e:
                print(f"读取文件{file_path}时发生错误：{str(e)}")
        
        self.names = list(self._prompt.keys())
        self.current_prompt = self._prompt[self.names[0]]
        
    def show_prompt_list(self):
        for i, name in enumerate(self.names, 1):
            print(f"{i}. {name}")
    
    def show_current_prompt(self, index=1):
        try:
            idx = int(index) - 1  # 转换为0-based索引
            if idx < 0 or idx >= len(self.names):
                raise ValueError("无效的索引")
            selected_name = self.names[idx]
            content = self._prompt[selected_name]
            print(content)
        except (ValueError, IndexError) as e:
            print(f"错误：{str(e)}，请检查输入的索引是否正确。")
    
    
    def set_current_prompt(self, index=1):
        try:
            idx = int(index) - 1
            if idx < 0 or idx >= len(self.names):
                raise ValueError("无效的索引")
            selected_name = self.names[idx]
            self.current_prompt = self._prompt[selected_name]
            print(f"已设置当前提示为：{selected_name}")
        except (ValueError, IndexError) as e:
            print(f"错误：{str(e)}，请检查输入的索引是否正确。")
    
    @property
    def prompt(self):
        return self.current_prompt