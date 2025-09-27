import allure
import pytest

from unit_tools.apiutils_single import RequestsBase
from unit_tools.handle_data.yaml_handler import read_yaml

req = RequestsBase()
@allure.feature("产品管理")
class TestGetProductManager:
    @allure.story('获取产品列表')
    @pytest.mark.parametrize('base_info,test_case', read_yaml('./data/getProductList.yaml'))
    def test_get_product_list(self, base_info,test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)

    @allure.story('获取产品详情')
    @pytest.mark.parametrize('base_info,test_case',read_yaml('./data/getProductDetails.yaml'))
    def test_get_product_details(self, base_info,test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)


