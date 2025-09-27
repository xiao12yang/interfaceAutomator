import allure
import pytest

from unit_tools.apiutils_business import RequestsBase
from unit_tools.handle_data.yaml_handler import read_yaml
from unit_tools.generate_id import m_id,t_id


@allure.feature(next(m_id)+'电子商务管理系统订单支付业务管理')
class TestProductBusiness:
    @pytest.mark.parametrize('api_info',read_yaml('./data/productScenario.yaml'))
    @allure.story(next(t_id)+'下单支付流程')
    def test_product_business_scenario(self,api_info):
        allure.dynamic.title(api_info['baseInfo']['api_name'])
        RequestsBase().execute_test_case(api_info)
