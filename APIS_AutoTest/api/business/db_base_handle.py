# create by: wangyun
# create at: 2020/4/23 22:28

from api.utils.db_utils import DBUtils

"""
数据库操作
"""


def search_intf_addr():
    """
    t_config_001_intf_address接口地址映射表，记录查询
    :return: 查询结果
    """
    sql = 'select intf_code, intf_addr from t_config_001_intf_address'

    return DBUtils().search(sql, [])


def add_lc_business_result(value_list):
    """
    t_result_001_scene_case_report 业务场景用例执行结果表，插入数据
    :param value_list:
    :return:
    """
    # 数据库添加记录
    sql = 'insert into t_result_001_scene_case_report(id, create_time, report_no, scene_name, step, request_url, request_body, respond_body, assert, remark) values (null, now(), %s, %s, %s, %s, %s, %s, %s, %s);'
    if isinstance(value_list, list) and len(value_list) == 15:
        DBUtils().add(sql, value_list)
    else:
        print('插入数据库，传入参数不满足要求。')


def search_lc_business_result(report_no):
    """
    t_result_001_scene_case_report 业务场景用例执行结果表，根据报告号查询结果
    :param report_no:
    :return:
    """
    # 数据库添加记录
    sql = 'select * from t_result_001_scene_case_report where report_no = %s order by id;'
    if isinstance(report_no, list):
        return DBUtils().search(sql, report_no)
    else:
        print('查询数据库，传入参数不满足要求。')


def get_lc_business_result_head():
    """
    t_result_001_scene_case_report 业务场景用例执行结果表，获取表头（多级表头）
    """
    # 数据库添加记录
    sql = 'select column_comment, column_name from information_schema.columns where table_name="t_result_001_scene_case_report";'
    return DBUtils().search(sql, [])


def search_late_report_no():
    """
    t_result_001_scene_case_report 业务场景用例执行结果表，获取最新的报告号
    :return:
    """
    sql = 'select distinct report_no from t_result_001_scene_case_report order by report_no desc limit 1;'
    return DBUtils().search(sql, [])


def search_fail_test_scene(report_no):
    """
    t_result_001_scene_case_report 业务场景用例执行结果表，根据传入的报告号，获取执行失败的场景
    :return:
    """
    sql = 'select distinct scene_name from t_result_001_scene_case_report where report_no=%s and assert="False";'
    return DBUtils().search(sql, [report_no, ])


if __name__ == '__main__':
    # print(len(search_lc_business_result(['20200425115810', ])))
    print(get_lc_business_result_head())
