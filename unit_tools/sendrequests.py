# 封装requests
import re
import requests
import json
from unit_tools.handle_data.yaml_handler import read_yaml,write_yaml
from unit_tools.log_util.recordlog import logs

class SendRequest:
    def __init__(self):
        pass

    @classmethod
    def _text_encode(cls, res_text):
        """
        处理接口返回值出现Unicode编码，如\\u767b\\
        :param res_text:
        :return:
        """
        match = re.search(r"\\u[0-9a-fA-F]{4}]",res_text)
        if match:
            return res_text.encode().decode('unicode-escape')
        else:
            return res_text

    def send_request(self, **kwargs):
        session = requests.Session()
        response = None
        try:
            response = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(response.cookies)
            res = self._text_encode(response.text)
            if set_cookie:
                # print(f"获取到cookie：{set_cookie}")
                write_yaml({'cookies':set_cookie})

            # print(res)
        except requests.exceptions.ConnectionError as e:
            logs.error('接口连接异常，可能是request的链接数过多或者速度过快导致程序报错')
        except requests.exceptions.RequestException as e:
            logs.error(f'接口请求异常，请检查系统或数据是否正常，原因：{e}')

        return response

    def execute_api_request(self, api_name, url, method, headers, case_name, cookies=None, files=None, **kwargs):
        """
        执行发起接口请求
        :param api_name: 接口名称
        :param url: 接口地址
        :param method: 请求方法
        :param header: 请求头
        :param case_name: 测试用例名称
        :param cookie: cookie
        :param file: 文件上传
        :param kwargs: 未知数量的关键字参数
        :return:
        """
        logs.info(f'接口名称：{api_name}')
        logs.info(f'请求地址：{url}')
        logs.info(f'请求方法：{method.upper()}')
        logs.info(f'请求头：{headers}')
        logs.info(f'用例名称：{case_name}')
        logs.info(f'Cookies：{cookies}')
        logs.info(f'files：{files}')
        # logs.info(f'')
        yaml_params_type = kwargs.keys()
        if kwargs and ('data' in yaml_params_type or 'json' in yaml_params_type or 'params' in yaml_params_type):
            params_type = list(kwargs.keys())[0]
            logs.info(f'参数类型：{params_type}')
            params = json.dumps(list(kwargs.values())[0],ensure_ascii=False)
            logs.info(f'请求参数：{params}')
            pass
        return self.send_request(method=method,
                                 url=url,
                                 headers=headers,
                                 cookies=cookies,
                                 files=files,
                                 timeout=10,
                                 verify=False,
                                 **kwargs)

if __name__ == '__main__':

    from unit_tools.handle_data.configParse import config
    data = read_yaml('../data/login.yaml')[0]
    url = config.get_host('host') + data["baseInfo"]['url']
    method = data["baseInfo"]['method']
    header = data["baseInfo"]['headers']
    req_data = data["testCases"][0]["data"]
    send = SendRequest()
    res = send.execute_api_request(api_name=None,url=url,method=method,headers=None,case_name=None,data=req_data)
    res_json = res.json()
    cookies = requests.utils.dict_from_cookiejar(res.cookies)
    token = res_json['token']
    userId = res_json['userId']
    if cookies:
        write_yaml({'Cookie':cookies,'token':token,'userId':userId})
    else:
        write_yaml({'token':token,'userId':userId})
    print(res)