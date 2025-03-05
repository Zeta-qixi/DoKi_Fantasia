class FileHandler:
    @staticmethod
    def read(path, encoding='utf-8'):

        try:
            with open(path, 'r', encoding=encoding) as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"文件 {path} 未找到。")
            return None
        except Exception as e:
            print(f"读取文件 {path} 时发生错误：{e}")
            return None

    @staticmethod
    def write(path, content, mode = 'w', encoding='utf-8'):

        try:
            with open(path, mode, encoding=encoding) as file:
                file.write(content)
            print(f"已成功将内容写入文件 {path}")
        except Exception as e:
            print(f"写入文件 {path} 时发生错误：{e}")

