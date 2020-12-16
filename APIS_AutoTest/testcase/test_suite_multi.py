# create by: wangyun
# create at: 2020/4/18 11:48
from api.comm.base_func import get_report_no, remove_file, make_system_name_file, html_to_pdf
from api.business.db_base_handle import search_lc_business_result, get_lc_business_result_head
from testcase.base_test_suite import add_test_case, multi_run_test_suite
from api.utils.excel_handle import ExcelHandle
from api.utils.send_email import send_email2


def test_suite(system_name):
    """
    多线程执行测试用例，并发线程数max_workers在init.yaml文件中设置，默认5
    :param system_name:
    :return:
    """
    # 生成文件
    make_system_name_file(system_name)
    # 扫描测试用例
    discover = add_test_case('./test_lc_business/')
    report_no = get_report_no()
    print(report_no)
    
    # 执行用例，生成html报告
    for i in discover:
        multi_run_test_suite(i, report_no, system_name, '业务流程测试用例'+report_no)

    # 生成详细结果excel文件
    data = search_lc_business_result([report_no, ])
    head = get_lc_business_result_head()
    ExcelHandle().make_excel_file(data, head, 'TestCase_details.xlsx', report_no)

    # 将html转换为pdf
    html_to_pdf(report_no, system_name)
    # 发送邮件
    send_email2(report_no)
    remove_file('report_no.txt')
        

if __name__ == '__main__':
    test_suite('addr-uat-out')
