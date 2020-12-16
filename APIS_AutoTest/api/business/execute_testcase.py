# create by: wangyun
# create at: 2020/4/29 23:39
import os

from api.comm.base_func import get_file_full_path
from api.comm.intf_request import RequestBase
from api.comm.request_respond_handle import ReqResHandle
from api.intf_case.intf_base_handle import intf_base_assert
from config.config_path import details_path, data_path
from api.intf_case.intf_init_engine import IntfInitEngine
from api.utils.excel_handle import ExcelHandle, style
from api.utils.read_yaml import ReadYaml


class ExecuteTestCase:

    def __init__(self, system_addr, excel_name, sheet_name=None):
        """
        执行用例
        :param system_addr: 环境名称，对应init.yaml中配置的参数名
        :param excel_name: data路径测试用例excel表格名称，.xls后缀
        :param sheet_name: excel表格页签名称，默认第一个页签
        """
        self.system_addr = system_addr
        self.excel_path = os.path.join(data_path, excel_name)
        self.sheet_name = sheet_name
        # 字典：所有场景；列表：场景顺序
        self.scene_all = dict()
        self.scene_index = list()

    def start_run(self, save_file):
        """
        开始执行测试用例
        :param save_file: 测试用例执行结果保存文件名称
        :return:
        """
        # 1. 第一步读取excel数据，读取模板
        excel_data = ExcelHandle().read_excel_data(self.excel_path, self.sheet_name)
        template_list = ExcelHandle().copy_excel_template(self.excel_path, self.sheet_name)
        template_book = template_list[0]
        template = template_list[1]

        nrows = len(excel_data)
        # 2. 获取所有场景及对应的步骤数，并存到字典中; 使用列表按顺序存放场景名称，执行时按此顺序
        for n in range(nrows):
            # 读取 业务场景编号
            scene_code = excel_data[n][1]
            # 场景编号不能为空
            if scene_code == '':
                break
            # 添加到 列表中
            if scene_code not in self.scene_index:
                self.scene_index.append(scene_code)
            # 将场景及对应的步骤数添加到字典中
            if scene_code not in self.scene_all.keys():
                self.scene_all[scene_code] = 1
            else:
                self.scene_all[scene_code] += 1
        # 3. 场景循环处理
        # 行 计数器，用于记录当前执行的行索引值
        row = 0
        # 第一重循环，按场景
        for scene in self.scene_index:
            # 提取响应参数存储的字典，场景开始前初始化
            response_after = dict()
            # 从字典中获取当前场景步骤数
            step_num = self.scene_all[scene]
            # 第二重循环，按步骤
            for step in range(1, step_num + 1):
                # 行索引计数器开始计数
                row += 1
                # 4. 读取导入excel的各个字段数据
                # 是否执行
                is_execute = excel_data[row-1][14]
                # 判断用例是否执行
                if is_execute.lower() != 'yes':
                    continue

                # 拼接接口请求url
                req_url = ReadYaml().get_value(self.system_addr) + excel_data[row-1][7]
                # 5. 开始执行
                try:
                    # 请求初始化
                    req_body = IntfInitEngine().start_init_engine(excel_data[row-1][8], excel_data[row-1][4], excel_data[row-1][10], **response_after)

                    # 执行请求
                    res = RequestBase(excel_data[row-1][6], req_url, req_body, eval(excel_data[row-1][9])).get_respond()
                    res_head = res.headers
                    if res.content:
                        res_body = res.text
                    else:
                        res_body = ''

                    # 断言
                    if res_body == '':
                        assert_result, remark = 'False', '无响应信息'
                    else:
                        assert_result, remark = intf_base_assert(excel_data[row-1][8], res_body, eval(excel_data[row-1][15]))

                    # 后置条件 提取参数
                    if excel_data[row-1][12]:
                        response_after = ReqResHandle(excel_data[row-1][8], res_body, excel_data[row-1][12], response_after).get_fields_value()
                    # 写入excel中
                    template.write(row, 15, req_body, style('style2'))
                    template.write(row, 16, str(res_head), style('style2'))
                    template.write(row, 17, res_body, style('style2'))
                    template.write(row, 18, str(response_after), style('style2'))
                    template.write(row, 19, assert_result, style('style2'))
                    template.write(row, 20, remark, style('style2'))
                except:
                    # 写入excel中
                    template.write(row, 20, '未知异常，执行失败', style('style2'))
        # 保存文件
        file_name = get_file_full_path(details_path, save_file, name2=self.system_addr)
        template_book.save(file_name)
