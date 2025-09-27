import pytest
from unit_tools.log_util.recordlog import logs
@pytest.fixture(autouse=True)
def print_info():
    logs.info('——————接口测试——————start')
    yield
    logs.info('——————接口测试——————end')
