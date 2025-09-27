import allure
import pytest

from unit_tools.handle_data.yaml_handler import read_yaml
from unit_tools.apiutils_single import RequestsBase
req = RequestsBase()

@allure.feature('物流管理')
class TestLogisticsMode:
    @allure.story('获取物料信息')
    @pytest.mark.parametrize('base_info,test_case',read_yaml('./data/getMaterial.yaml'))
    def test_get_material_info(self, base_info,test_case):
        allure.dynamic.title(test_case['case_name'])
        req.execute_test_case(base_info, test_case)
