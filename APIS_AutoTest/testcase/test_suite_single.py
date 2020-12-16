# create by: wangyun
# create at: 2020/4/18 11:48
import unittest
import HTMLTestReportCN
from api.comm.base_func import get_report_no, get_file_full_path, remove_file, make_system_name_file
from api.business.db_base_handle import search_lc_business_result, get_lc_business_result_head
from config.config_path import report_path
from api.utils.excel_handle import ExcelHandle
from api.utils.send_email import send_email


def test_suite(system_name):
    """

    :param system_name:
    :return:
    """
    # 生成文件
    make_system_name_file(system_name)
    # 扫描测试用例
    discover = unittest.defaultTestLoader.discover('./test_lc_business/', pattern='test*.py')
    report_no = get_report_no()
    print(report_no)
    # 生成html报告
    html_name = get_file_full_path(report_path, 'result.html', report_no, system_name)
    fp = open(html_name, 'wb')
    runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title='业务流程执行报告'+report_no, tester='wyun')
    runner.run(discover)
    fp.close()
    # 生成详细结果excel文件
    data = search_lc_business_result([report_no, ])
    head = get_lc_business_result_head()
    ExcelHandle().make_excel_file(data, head, 'TestCase_details.xls', report_no)
    # 发送邮件
    send_email(report_no)

    remove_file('report_no.txt')


if __name__ == '__main__':
    test_suite('addr-uat-out')
