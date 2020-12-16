# create by: wangyun
# create at: 2020/3/29 16:26
import os

# 当前路径: config
config_path = os.path.abspath(os.path.dirname(__file__))
# 项目所在路径
project_path = os.path.dirname(config_path)

# data目录所在路径
data_path = os.path.join(project_path, 'data')
# result目录所在路径
result_path = os.path.join(project_path, 'result')
# temp临时目录所在路径
temp_path = os.path.join(project_path, 'temp')

# 初始化配置
init_file = os.path.join(config_path, 'init.yaml')
# 公共参数配置
comm_file = os.path.join(config_path, 'comm.yaml')

# report目录所在路径
report_path = os.path.join(result_path, 'report')
# report目录所在路径
report_pdf_path = os.path.join(result_path, 'report_pdf')
# details目录所在路径
details_path = os.path.join(result_path, 'details')
# log目录所在路径
log_path = os.path.join(result_path, 'log')

