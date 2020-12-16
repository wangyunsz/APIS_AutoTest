# create by: wangyun
# create at: 2020/4/23 22:08
import os
import pdfkit

from config.config_path import temp_path, report_path, report_pdf_path
from api.utils.read_yaml import ReadYaml
from api.utils.time_style import TimeStyle

"""
公共函数类
"""


# 从文件中获取一个批次号，如果没有该文件，则生成批次号，并保存到一个文件中
def get_report_no():
    """
    从文件中获取一个批次号，如果没有该文件，则生成批次号，并保存到一个文件中
    :return: report_no 执行批次号
    """
    file = os.path.join(temp_path, 'report_no.txt')
    if not os.path.exists(file):
        with open(file, 'w', encoding='UTF-8') as f:
            report_no = TimeStyle().cur_time
            f.write(report_no)
        f.close()
        return report_no
    with open(file, 'r') as f:
        report_no = f.read().strip()
    f.close()
    return report_no


def make_system_name_file(value):
    """
    生成系统名称的文件，用于测试用例执行时自动获取
    :param value:
    :return:
    """
    file = os.path.join(temp_path, 'system_name.txt')
    if os.path.exists(file):
        remove_file(value)
    with open(file, 'w', encoding='UTF-8') as f:
        f.write(value)
    f.close()


def remove_file(file_name):
    """
    删除文件
    :param file_name: temp目录下文件名称
    """
    if os.path.exists(os.path.join(temp_path, file_name)):
        os.remove(os.path.join(temp_path, file_name))


def get_file_full_path(host_path, file_name, report_no=None, name2=None):
    """
    获取文件完整路径（加上日期目录层级）
    :param host_path: 主路径
    :param file_name: 文件名称
    :param report_no: 报告号（时间戳标识）
    :param name2: 标识，如：dev、sit、uat
    :return: 包含日期层级目录的完整路径
    """
    if name2 is None:
        name2 = ''

    cur_date_path = os.path.join(host_path, TimeStyle().cur_date)
    if not os.path.exists(cur_date_path):
        os.mkdir(cur_date_path)

    if report_no is None:
        new_file_name = file_name.split('.')[0] + '_' + name2 + '_' + TimeStyle().cur_time + '.' + file_name.split('.')[1]
    else:
        new_file_name = file_name.split('.')[0] + '_' + name2 + '_' + report_no + '.' + file_name.split('.')[1]

    return os.path.join(cur_date_path, new_file_name)


def get_host_date_path(host_path):
    """
    获取某个路径下当前日期文件夹，没有则创建
    :param host_path: 主目录
    :return: 日期文件夹路径
    """
    cur_date_path = os.path.join(host_path, TimeStyle().cur_date)
    if not os.path.exists(cur_date_path):
        os.mkdir(cur_date_path)
    return cur_date_path


def get_report_no_file(report_no, host_path):
    """
    根据报告号获取对应目录的文件，用于获取测试结果文件完整路径（html、details）
    :param report_no: 报告号
    :param host_path: 目标目录
    :return: 文件完整路径
    """
    file = ''
    cur_date_path = os.path.join(host_path, report_no[:8])
    for i in os.listdir(cur_date_path):
        if report_no in i:
            file = i
    return os.path.join(cur_date_path, file)


def html_to_pdf(report_no, system_name):
    """
    将 html 页面转换为 pdf，注意：需要本地安装wkhtmltopdf.exe，并设置路径才能转换pdf
    :param report_no: 报告号
    :param system_name: 系统名称
    """
    path_wk = ReadYaml().get_value('wkhtmltopdf_path')
    html_file_path = get_report_no_file(report_no, report_path)
    pdf_file_path = get_file_full_path(report_pdf_path, 'report.pdf', report_no, system_name)
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    with open(html_file_path, 'r', encoding='utf-8') as f:
        pdfkit.from_file(f, pdf_file_path, configuration=config)
        f.close()


if __name__ == '__main__':
    html_to_pdf('20200502173942', 'addr-uat-out')