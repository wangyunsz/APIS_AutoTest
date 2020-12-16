# create by: wangyun
# create at: 2020/4/20 20:01
import os
import xlrd
from concurrent.futures import ThreadPoolExecutor
from api.comm.request_respond_handle import ReqResHandle
from api.comm.intf_request import RequestBase
from api.utils.db_utils import DBUtils
from api.utils.read_yaml import ReadYaml
from api.utils.time_style import TimeStyle
from config.config_path import data_path
from api.intf_case.intf_init_engine import IntfInitEngine

"""
多线程实现请求（某个固定业务场景使用，已废弃）
"""


def func_handle(param):
    """
    多线程处理函数
    :param report_no: 报告号
    :param num: 序号
    :param url: 请求地址
    :param req_body: 请求体
    """
    report_no, num, url, req_body = param
    request_type = 'post'
    headers = {"Content-Type": "text/plain; charset=UTF-8"}
    data_type = 'xml'
    # 1. 请求
    respond = RequestBase(request_type, url, req_body, headers).get_respond_body()
    # 2.获取各字段值

    # 3.数据库添加记录
    sql = 'insert into t_result_001_scene_case_report(id, create_time, report_no, step, request_url, request_body, respond_body, remark) values (null, now(), %s, %s, %s, %s, %s, %s);'
    # 备注信息（手工调整）
    remark = ''
    value_list = [report_no, num, url, req_body, respond, remark]

    DBUtils().add(sql, value_list)


def multi_execute(sys_addr, file_name):
    # 相关参数初始化
    # 设置线程数（在init文件中设置）
    executor = ThreadPoolExecutor(max_workers=20)
    # 接口编号与接口地址对应关系字典，===内容已删除===
    url_dict = {}
    report_no = TimeStyle().cur_time
    print(report_no)
    file_path = os.path.join(data_path, file_name)

    # excel读取报文
    book = xlrd.open_workbook(file_path)
    tp_table = book.sheet_by_index(0)

    nrows = tp_table.nrows

    print('==============开始读取数据，共计[%s]条==============' % nrows)
    req_msg_list = []
    for i in range(nrows):
        req_msg = ''
        if i < 1:
            continue
        req_msg = tp_table.cell(i, 3).value
        # 读取接口代码
        req_code = ReqResHandle('xml', req_msg, 'RequestType').get_fields_value().get('RequestType')
        # 接口地址

        intf_url = ReadYaml().get_value(sys_addr) + url_dict.get(req_code)
        # 请求初始化
        req_msg = IntfInitEngine().start_init_engine('xml', req_code, req_msg)

        req_msg_list.append((report_no, str(i), intf_url, req_msg))

    print('==============读取数据完成，开始多线程执行==================')
    for n in range(len(req_msg_list)):
        executor.submit(func_handle, req_msg_list[n])


if __name__ == '__main__':
    multi_execute('addr-uat-out', 'xxx.xls')
