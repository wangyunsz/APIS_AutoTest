# create by: wangyun
# create at: 2020/4/25 10:07
import pandas as pd
import xlrd
import xlwt
from xlutils.copy import copy
from api.comm.base_func import get_file_full_path
from config.config_path import details_path
"""
Excel操作工具类
"""


def style(name):
    font = xlwt.Font()
    font.name = u'宋体'

    # 字体居中
    alignment1 = xlwt.Alignment()
    alignment1.horz = 2  # 水平对齐-居中
    # 字体靠左
    alignment2 = xlwt.Alignment()
    alignment2.horz = 1  # 水平对齐-靠左

    # 边框线
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40

    # 样式一：水平居中，边框线，（数值）
    style1 = xlwt.XFStyle()
    style1.font = font
    style1.alignment = alignment1
    style1.borders = borders
    style1.num_format_str = '0'

    # 样式二：水平靠左，边框线
    style2 = xlwt.XFStyle()
    style2.font = font
    style2.alignment = alignment2
    style2.borders = borders

    if name == 'style1':
        return style1
    else:
        return style2


class ExcelHandle:

    def __init__(self):
        """
        Excel操作工具类，支持功能：从excel读取数据、将数据导出到excel
        """
        self.export_excel_path = details_path

    def read_excel_data(self, excel_path, sheet_name=None):
        """
        读取excel中的数据
        :param excel_path: excel路径
        :param sheet_name: 页签名称，默认第一个
        :return: 列表
        """
        wbook = xlrd.open_workbook(excel_path)
        if sheet_name is None:
            wsheet = wbook.sheet_by_index(0)
        else:
            wsheet = wbook.sheet_by_name(sheet_name)
        row = wsheet.nrows
        result = []
        for i in range(row):
            if i < 1:
                continue
            row_values = wsheet.row_values(i)
            result.append(row_values)
        return result

    def make_excel_file(self, data, head, file_name, report_no=None):
        """
        将数据导出到exce文件
        :param data: 数据，元组
        :param head: 表头，元组
        :param file_name: excel名称，包含后缀.xlsx/.xls
        :param report_no: 时间戳标识
        :return:
        """
        file_path = get_file_full_path(self.export_excel_path, file_name, report_no)
        # pandas实现（使用一段时间后莫名报错）
        # df = pd.DataFrame(list(zip(*data)), columns=head)
        # df.to_excel(excel_writer=file_path, sheet_name='Sheet1')

        # xlwt实现
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        if len(head) > 1:
            head_col = len(head)
        else:
            head_col = 1
        # 写入表头
        for i in range(head_col):
            if len(head) == 0:
                continue
            for j in range(len(head[i])):
                ws.write(i, j, head[i][j])
        # 写入数据
        row = len(data)
        if row == 0:
            print('无数据写入表格。')
            return None
        for r in range(row):
            for c in range(len(data[r])):
                ws.write(r+head_col, c, str(data[r][c]))
        wb.save(file_path)

        return file_path

    def copy_excel_template(self, template_path, sheet_name=None):
        """
        复制模板，用于写入数据后保存
        :param template_path:
        :param sheet_name:
        :return:
        """
        template = xlrd.open_workbook(template_path, formatting_info=True)
        # 复制模板（用于写入数据并到处）
        wbook = copy(template)
        if sheet_name:
            return wbook, wbook.sheet_by_name(sheet_name)
        else:
            return wbook, wbook.get_sheet(0)
