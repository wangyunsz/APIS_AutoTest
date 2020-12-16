# create by: wangyun
# create at: 2020/5/2 9:44
import HTMLTestReportCN
import unittest

from BeautifulReport import BeautifulReport
from tomorrow import threads
from api.comm.base_func import get_file_full_path, get_host_date_path
from config.config_path import report_path
from api.utils.read_yaml import ReadYaml


def add_test_case(test_path, pattern='test*.py'):
    """
    扫描并添加测试用例
    :param test_path: 执行的测试用例所在的路径
    :param pattern: 扫描用例匹配的规则
    :return: discover
    """
    return unittest.defaultTestLoader.discover(test_path, pattern=pattern)


def run_test_suite(discover, report_no, system_name, title=None):
    """
    执行测试集
    :param discover: 所有测试用例
    :param report_no: 测试执行批次号（时间戳）
    :param system_name: 系统名称
    :param title: 测试报告标题
    """
    html_name = get_file_full_path(report_path, 'result.html', report_no, system_name)
    fp = open(html_name, 'wb')
    runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title=title, tester='wyun')
    runner.run(discover)
    fp.close()


@threads(ReadYaml().get_value('max_workers'))
def multi_run_test_suite(discover, report_no, system_name, case_name):
    """
    多线程执行用例
    :param discover: 所有测试用例
    :param report_no: 测试执行批次号（时间戳）
    :param system_name: 系统名称
    :param case_name: 用例名称
    """
    cur_date_path = get_host_date_path(report_path)
    file_name = 'result_' + system_name + '_' + report_no + '.html'
    result = BeautifulReport(discover)
    result.report(filename=file_name, description=case_name, log_path=cur_date_path)
