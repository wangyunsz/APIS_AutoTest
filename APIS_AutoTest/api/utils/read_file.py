# create by: wangyun
# create at: 2020/4/1 21:24
import os


class ReadFile:
    """
    读取文件内容
    """
    def __init__(self, file_name, file_dir):
        self.file_name = file_name
        self.file_dir = file_dir
        self.file_path = os.path.join(self.file_dir, self.file_name)

    def get_file_value(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                result = f.read()
                f.close()
                return result
        else:
            print('读取文件路径[%s]不存在。' % self.file_path)
            return ''
