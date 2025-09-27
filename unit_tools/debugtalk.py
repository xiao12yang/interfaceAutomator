# 对接口信息yaml文件进行解析、参数加密、获取当前时间等
import random
import re
import time

from unit_tools.handle_data.yaml_handler import get_extract_yaml
class DebugTalk:
    def get_extract_data(self,node_name,out_format=None):
        """
        获取extract.yaml数据，首先判断out_format是否为数字，如果是数字说明是读取数组，如果不是数字就是读取下一个节点的value
        :param data_name: extract.yaml文件中的key
        :param out_format: str类型，四种情况：0为随机读取，-1为读取全部数据返回的是字符串格式，-2为读取全部数据，返回的是列表格式，其他值就按顺序读取
        :return:
        """
        data = get_extract_yaml(node_name)
        if out_format is not None and bool(re.compile(r'^[+-]?\d+$').match(str(out_format))):
            out_format = int(out_format)
            # 设置匹配情况,集合不会出现重复的key，后来者会覆盖
            data_value = {
                out_format: self.seq_read(data,out_format),
                0:random.choice(data),
                -1:','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[out_format]
        else:
            data = get_extract_yaml(node_name,out_format)
        return data


    def seq_read(self,data,randoms):
        if randoms < -2:
            raise Exception('索引出错，取值范围为[-2,max)')
        if randoms > 0:
            return data[randoms - 1]
        else:
            return None


    def get_now_time(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def get_now_date(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def get_timeStamp(self):
        return time.time()

    def get_headers(self,params_type):
        """
        获取请求头的类型
        :param params_type: 参数类型：如"data"、"json"
        :return:
        """
        header_mapping = {
            'data': {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
            'json': {'Content-Type': 'application/json;charset=UTF-8'},
        }
        header = header_mapping.get(params_type)
        if header is None:
            raise ValueError('不支持其他类型的请求头')
        return header



if __name__ == '__main__':
    debugtalk = DebugTalk()
    print(debugtalk.get_extract_data("goodsId",-3))