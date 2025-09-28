import allure
import pytest

from unit_tools.apiutils_business import RequestsBase
from unit_tools.handle_data.yaml_handler import read_yaml

@allure.feature('电子商务管理系统用户下订单业务管理')
class TestCreateOrderScenario:
    @pytest.mark.parametrize('api_info',read_yaml('./data/createOrderScenario.yaml'))
    @allure.dynamic.title('用户下订单流程')
    def test_create_order_scenario(self,api_info):
        allure.dynamic.title(api_info['baseInfo']['api_name'])
        RequestsBase().execute_test_case(api_info)

