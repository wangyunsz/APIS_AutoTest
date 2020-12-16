import logging
import datetime
import os

# 定义日志级别的映射
from config.config_path import log_path
from api.utils.read_yaml import ReadYaml
from api.utils.time_style import TimeStyle

log_level_mapper = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}


class Logger:
    # 输出文件名称，Logger_name，日志级别
    def __init__(self, log_file, log_name, log_level):
        self.log_file = log_file    # 扩展名 配置文件
        self.log_name = log_name    # 参数
        self.log_level = log_level.lower()  # 配置文件
        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置log级别
        self.logger.setLevel(log_level_mapper[self.log_level])   # logging.INFO
        # 判断handlers是否存在
        if not self.logger.handlers:
            # 输出控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_level_mapper[self.log_level])
            formatter = logging.Formatter('[%(asctime)s][%(thread)s][%(levelname)s]: %(message)s')
            fh_stream.setFormatter(formatter)
            # 写入文件
            fh_file = logging.FileHandler(self.log_file)
            fh_file.setLevel(log_level_mapper[self.log_level])
            fh_file.setFormatter(formatter)

            # 添加handler
            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)


# 当前时间
current_time = TimeStyle().cur_date

# 扩展名
log_extension = ReadYaml().get_value('log.extension')
logfile = os.path.join(log_path, current_time+log_extension)

# 日志文件级别
level = ReadYaml().get_value('log.level')


# 对外调用该方法，写入日志
def my_log(log_name=__file__):
    return Logger(log_file=logfile, log_name=log_name, log_level=level).logger


if __name__ == "__main__":
    my_log().debug("this is a debug")
    my_log().info('this is a info.')
    my_log().error('error....')