import allure
import pytest
from unit_tools.apiutils_single import RequestsBase
from unit_tools.generate_id import m_id,t_id
from unit_tools.handle_data.yaml_handler import read_yaml
from unit_tools.handle_data.configParse import config
from unit_tools.sendrequests import SendRequest

conf = config
send = SendRequest()
req = RequestsBase()

@allure.feature(next(m_id)+"系统用户管理模块")
@allure.issue(url='http://www.baidu.com')
class TestUserManager:
    """登录模块"""
    @allure.story(next(t_id)+'新增用户')
    @pytest.mark.parametrize('base_info,test_case', read_yaml('./data/adduser.yaml'))
    def test_add_user(self, base_info, test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)

    @allure.story(next(t_id)+'删除用户')
    @pytest.mark.parametrize('base_info,test_case', read_yaml('./data/deleteUser.yaml'))
    def test_delete_user(self, base_info, test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)

    @allure.story(next(t_id)+'查询用户')
    # @allure.step('读取yaml文件，发送requests请求，对比返回结果')
    @pytest.mark.parametrize('base_info,test_case', read_yaml('./data/queryUser.yaml'))
    def test_query_user(self, base_info, test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)

    @allure.story(next(t_id)+'修改用户')
    @pytest.mark.parametrize('base_info,test_case', read_yaml('./data/updateUser.yaml'))
    def test_update_user(self, base_info, test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)

