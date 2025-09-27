import pytest
import requests.utils
import allure

from unit_tools.handle_data.yaml_handler import read_yaml, write_yaml
from unit_tools.handle_data.configParse import config
from unit_tools.sendrequests import SendRequest
from unit_tools.apiutils_single import RequestsBase
conf = config
send = SendRequest()

req = RequestsBase()
@allure.feature('登录模块')
class TestLogin:
    """登录模块"""
    @allure.story('验证登录')
    # @allure.title('用户登录成功')
    @allure.description('这是系统模块里面的登录功能，需要验证正确的data是否登录成功')
    @pytest.mark.parametrize('base_info,test_case',read_yaml('./data/login.yaml'))
    def test_login_module(self, base_info,test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)
        #
        # # 从yaml文件获取接口信息
        # conf_url = conf.get_host('host')
        # api_name = api_info['baseInfo']['api_name']
        # url = conf_url + api_info['baseInfo']['url']
        # method = api_info['baseInfo']['method']
        # headers = api_info['baseInfo']['headers']
        # case_name = api_info['testCases'][0]['case_name']
        # req_param = api_info['testCases'][0]['data']
        # # 接口请求去执行接口
        # response = send.execute_api_request(api_name=api_name,url=url,method=method,headers=headers,case_name=case_name,cookie=None,file=None,data=req_param)
        # # 将接口返回数据转化为json格式
        # result_json= response.json()
        # print(f'接口返回信息：{result_json}')
        # cookie = requests.utils.dict_from_cookiejar(response.cookies)
        # token = result_json['token']
        # userId = result_json['userId']
        # write_yaml({"Cookie":cookie,"token":token,"userId":userId})
        # assert result_json['msg'] == "登录成功",'登录接口测试失败'

if __name__ == '__main__':
    pytest.main(['-k','test_login'])
