# create by: wangyun
# create at: 2020/4/23 21:49
import unittest

from api.business.db_base_handle import search_intf_addr
from config.config_path import temp_path
from testcase.test_case.case_01_OTI_001_xxx import case_01_OTI_001
from api.utils.read_file import ReadFile

"""
XXX场景用例
"""


class TestOTIScene(unittest.TestCase):
    """
    XXX 测试用例类
    """
    def __init__(self, *args, **kwargs):
        super(TestOTIScene, self).__init__(*args, **kwargs)

        self.sys_addr = ReadFile('system_name.txt', temp_path).get_file_value()
        self.intf_url_dict = dict(search_intf_addr())

    def setUp(self):
        pass

    def test_001_scene(self):
        case_01_OTI_001(self.sys_addr, self.intf_url_dict)
    #
    # def test_002_scene(self):
    #     case_01_OTI_002(self.sys_addr, self.intf_url_dict)
    #
    # def test_003_scene(self):
    #     case_01_OTI_003(self.sys_addr, self.intf_url_dict)
    #
    # def test_004_scene(self):
    #     case_01_OTI_004(self.sys_addr, self.intf_url_dict)
    #
    # def test_005_scene(self):
    #     case_01_OTI_005(self.sys_addr, self.intf_url_dict)
    #
    # def test_006_scene(self):
    #     case_01_OTI_006(self.sys_addr, self.intf_url_dict)

    def tearDown(self):
        pass
