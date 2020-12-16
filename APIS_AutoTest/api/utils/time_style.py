# create by: wangyun
# create at: 2020/3/29 16:59
import time
from datetime import datetime, timedelta


# 计算两个日期之间间隔的天数
def get_dates(start_date, end_date):
    # 时间格式化
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y%m%d%H%M%S')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y%m%d%H%M%S')

    if isinstance(start_date, datetime) and isinstance(end_date, datetime):
        # 弱判断，如果终止日期与起始日期对应的时间不相等，则认为分别为：'000000'、'235959'；如果相等，则认为都是'000000'
        # 因为工具生成的终止日期时间为'235959'，所以需要进行时间补偿
        if start_date.hour != end_date.hour:
            end_date = end_date + timedelta(days=1)

        interval = datetime(end_date.year, end_date.month, end_date.day) - datetime(start_date.year, start_date.month, start_date.day)
        ds = interval.days
        if ds <= 365:
            return ds
        else:
            return 365
    else:
        print('start_date[%s], end_date[%s]参数转换时间格式错误。' % (start_date, end_date))
        return None


class TimeStyle:
    """
    时间工具类
    """
    def __init__(self, dates=None, back_date=None):
        # 期限天数
        self.dates = dates
        # 提前天数，None,0-不提前，默认第二天起
        self.back_date = back_date

        # 当前日期，年月日:YYYYMMDD
        self.cur_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 当前时间，年月日时分秒：YYYYMMDDHHMMSS
        self.cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    # 获取当天、第二天、一年后
    def get_time_insurance_period(self):
        time_now = datetime.now()

        # 不提前，默认第二天起
        if self.back_date is None or self.back_date == 0:
            start_time = time_now + timedelta(days=1)
        elif self.back_date < 0:
            start_time = time_now + timedelta(days=self.back_date+1)
        elif self.back_date > 0:
            start_time = time_now + timedelta(days=self.back_date+1)
        else:
            print('提前天数[格式错误]，按T+1方式，默认第二天起')
            start_time = time_now + timedelta(days=1)

        if isinstance(self.dates, int) and self.dates > 0:
            end_time = start_time + timedelta(days=self.dates-1)
        else:
            # 默认按平年处理，如果期限中包含闰年的2-29则还需+1
            end_time = start_time + timedelta(days=365-1)

        # 当天、第二天、一年后
        insure_time_str = time_now.strftime('%Y%m%d%H%M%S')
        start_time_str = start_time.strftime('%Y%m%d') + '000000'
        end_time_str = end_time.strftime('%Y%m%d') + '235959'

        return insure_time_str, start_time_str, end_time_str


