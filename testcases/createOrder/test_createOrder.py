import allure
import pytest

from unit_tools.handle_data.yaml_handler import read_yaml
from unit_tools.apiutils_single import RequestsBase

req = RequestsBase()
@allure.feature('订单管理模块')
class TestCreateOrder:
    @pytest.mark.parametrize('base_info,test_case',read_yaml('./data/createOrder.yaml'))
    def test_create_order(self, base_info,test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)