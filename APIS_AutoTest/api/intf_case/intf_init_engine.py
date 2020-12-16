# create by: wangyun
# create at: 2020/4/23 9:22
import json

from api.intf_case.intf_base_handle import intf_base_init

"""
接口初始化引擎
"""


class IntfInitEngine:

    def __init__(self):
        pass

    def start_init_engine(self, req_type, intf_code, req_body, **kwargs):
        """
        启动引擎，进行接口初始化
        :param req_type: 请求数据类型，如：json，xml
        :param intf_code: 接口编号，对应RequestType，如：A01，A02
        :param req_body: 请求体，即需要初始化的请求
        :param kwargs: 可变关键字参数，以键值对的方式传入值
        :return: req_body
        """
        #  =======注：此部分是针对不同接口的请求体中不能固定、每次执行需要动态生成的字段值（如：请求ID、日期、有重复校验的证件号和姓名等），
        #  =======    进行字段赋值的操作（可自行按不同接口定义对应的方法）
        # if req_type.upper() == 'XML':
        #     if intf_code == 'A01':
        #         req_body = intf_A01_init(req_type, req_body)
        #     elif intf_code in ['A02', 'B01']:
        #         req_body = intf_A02_init(req_type, req_body)
        #     else:
        #         print('初始化出错，接口编号无法匹配。')
        # elif req_type.upper() == 'JSON':
        #     if intf_code == 'D02':
        #         req_body = intf_D02_init(req_type, req_body)
        # else:
        #     print('初始化出错，接口数据类型无法匹配。')

        # 更新关联接口字段值
        req_body = intf_base_init(req_type, req_body, **kwargs)

        # 针对json格式数据，请求体格式做转换，将字典转换为json
        if isinstance(req_body, dict):
            req_body = json.dumps(req_body)

        return req_body





