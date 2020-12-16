# create by: wangyun
# create at: 2020/12/16 14:55
from api.business.execute_testcase import ExecuteTestCase


# 执行Excel接口用例，执行完成后在result-->details路径生成执行结果
if __name__ == '__main__':
    excel_name = '接口测试用例模板.xls'
    save_file = '测试用例执行结果.xls'
    system_addr = 'addr-uat'

    ExecuteTestCase(system_addr, excel_name).start_run(save_file)

