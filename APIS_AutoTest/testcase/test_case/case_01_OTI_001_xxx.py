# create by: wangyun
# create at: 2020/4/24 17:57
from api.comm.base_func import get_report_no
from api.business.db_base_handle import add_lc_business_result
from api.comm.intf_request import RequestBase
from api.comm.request_respond_handle import ReqResHandle
from config.config_path import comm_file, data_path
from api.intf_case.intf_init_engine import IntfInitEngine
from api.utils.read_file import ReadFile
from api.utils.read_yaml import ReadYaml


def case_01_OTI_001(sys_addr, intf_url_dict):
    data_type = 'xml'
    file_name = 'aaa.txt'
    headers = eval(ReadYaml(comm_file).get_value('headers'))
    report_no = get_report_no()
    # 请求体数据从文件中读取，可放入data_path下层目录
    req_body = ReadFile(file_name, data_path).get_file_value()
    # 读取接口代码
    req_code = ReqResHandle(data_type, req_body, 'RequestType').get_fields_value().get('RequestType')
    # 接口地址
    intf_url = ReadYaml().get_value(sys_addr) + intf_url_dict.get(req_code)

    scene_name, step, respond, assert_result, remark = None, None, None, None, None
    try:
        # 请求初始化
        req_body = IntfInitEngine().start_init_engine(data_type, req_code, req_body)

        # 执行请求
        respond = RequestBase('post', intf_url, req_body, headers).get_respond_body()

        # 获取当前函数的注释
        scene_name = case_01_OTI_001.__doc__.strip()
        step = 'step_01：xxx'
        remark = file_name

        # 断言，先从响应中获取对应字段的值，再进行比较
        assert_result = 'xxx'

    except:
        assert False
        pass
    finally:
        # 保存结果至数据库
        value_list = [report_no, scene_name, step, intf_url, req_body, respond,
                      assert_result, remark]
        add_lc_business_result(value_list)

