# create by: wangyun
# create at: 2020/3/29 17:14
import random


class RandomCode:

    def __init__(self, length):
        """
        随机字符串生成
        :param length: 字符串长度
        """
        self.length = length

    # 生成随机位数的数字字符串
    def random_num(self):
        ret_num = ''
        for i in range(self.length):
            ret_num += str(random.randint(0, 9))
        return ret_num

    # 生成随机字符串
    def random_str(self):
        full_choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        ret_num = ''
        for i in range(self.length):
            ret_num += random.choice(full_choice)
        return ret_num
