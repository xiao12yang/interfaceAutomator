import os
import sys

import pytest

# project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.insert(0, project_root)
from config.setting import DIR_PATH
from unit_tools.handle_data.yaml_handler import read_yaml
# data = read_yaml(DIR_PATH + '/data/login.yaml')

class TestParametrize:

    @pytest.mark.parametrize("user",[
        {'username':'123456','password':'abcdef'},
        {'username':'123456','password':'123456'},
        {'username':'1234561','password':'abcdef'}
    ])
    def test_login_001(self,user):
        assert (user.get("username") == '123456' and user.get('password') == 'abcdef'),'执行失败，用户名或密码错误'
    @pytest.mark.parametrize('username,password',[("123456","password"),("123457","password")])
    def test_login_002(self,username,password):
        print(username,password)

    @pytest.mark.parametrize('api_info',read_yaml('./data/login.yaml'))
    def test_login_003(self,api_info):
        print(api_info)
        assert False,api_info

if __name__ == '__main__':
    pytest.main(['-sv','-k','test_parametrize.py'])

