# 管理一些根目录和路径
import os
import sys
# 获取根目录
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# 分析当前的根目录，存储到系统路径中，以确保在不同环境下都能找到根目录下的文件
sys.path.append(DIR_PATH)

FILE_PATH = {
    'extract':os.path.join(DIR_PATH, 'extract.yaml'),
    'ini':os.path.join(DIR_PATH, 'config','config.ini'),
    'log':os.path.join(DIR_PATH,'logs')
}
# 钉钉机器人
# 是否发送钉钉消息
is_dd_msg = True
secret = 'SECccaf2ff601c590f5745c83bd88014610cb7f99a696b13e923de38468284d5da2'
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=b1b0a9d43da44c2812cd8dcd0bd1f55b8e4017bfd952eadffe0095482d032aef'
