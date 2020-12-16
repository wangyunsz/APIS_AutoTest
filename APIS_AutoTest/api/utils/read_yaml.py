# create by: wangyun
# create at: 2020/2/27 23:23
import yaml
from config.config_path import init_file


def get_any_value_step(node, temp, i=0):
    """
    递归函数
    :param node: 层级节点名称
    :param temp: 中间值
    :param i: 计数索引
    :return: 最终值
    """
    # 当前节点索引（负向）
    node_index = -len(node) + i
    if node_index == -1:
        return temp.get(node[-1])
    return get_any_value_step(node, temp.get(node[node_index]), i+1)


class ReadYaml:
    """
    读取yaml文件字段内容
    默认读取文件init.yaml
    """
    def __init__(self, file_path=init_file):
        self.file_path = file_path

    def get_yaml(self):
        """
        读取yaml文件
        :return: 字典
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        return file

    def get_value(self, level_name):
        """
        读取任意节点字段值
        :param level_name: 节点字段名，如：db.host
        :return: 字段值
        """
        if '.' not in level_name:
            return self.get_yaml().get(level_name)
        else:
            temp = self.get_yaml()
            node = level_name.split('.')
            return get_any_value_step(node, temp)

