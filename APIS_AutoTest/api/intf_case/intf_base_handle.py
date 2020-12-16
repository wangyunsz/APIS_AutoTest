# create by: wangyun
# create at: 2020/4/23 22:42
from api.comm.request_respond_handle import ReqResHandle


def intf_base_init(data_type, request_body, **kwargs):
    """
    接口初始化通用类：更新关联接口字段值
    :param data_type: 数据类型，如：xml，json
    :param request_body: 请求体
    :param kwargs: 可变关键字参数
    :return: 请求体
    """
    return ReqResHandle(data_type, request_body, kwargs.keys(), kwargs).update_fields_value()


def intf_base_assert(data_type, res_body, assert_dict):
    """
    断言
    :param data_type: 数据类型，如：xml，json
    :param res_body: 响应体
    :param assert_dict: 断言字段字典
    :return:
    """
    result = ''
    remark = ''
    if assert_dict is None:
        return '', ''

    # 遍历断言字典
    for key, value in assert_dict.items():
        item_value = ReqResHandle(data_type, res_body, key).get_fields_value()
        if item_value:
            if value == item_value:
                result = 'True'
            else:
                result = 'False'
                remark += '断言[%s]等于[%s]失败，实际等于[%s]；'.format(key, value, item_value)
        else:
            result = 'False'
            remark += '断言[%s]等于[%s]失败，实际未获取到值或获取为空；'.format(key, value, item_value)

    return result, remark
