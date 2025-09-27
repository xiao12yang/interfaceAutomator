import pytest

# 定义夹具
# 不带函数的fixture夹具
# @pytest.fixture
# def setup_and_teardown():
#     print('测试函数执行前执行的前置操作')
#     yield '666'
#     print('测试函数执行后执行的后置操作')


# @pytest.fixture(scope='function',autouse=True)
# def setup_and_teardown():
#     print('测试函数执行前执行的前置操作')
#     yield '666'
#     print('测试函数执行后执行的后置操作')
#
# @pytest.fixture(scope='function',autouse=True,params=['广东','广西'],name='setValue',ids=['GD','GX'])
# def set_params(request):
#     return request.param





class TestFixture:
    def test_case_001(self):
        print(f'这是第一个测试用例，夹具返回值 --- ')

    def test_case_002(self):
        print(f'这是第二个测试用例')

    def test_case_003(self):
        print(f'这是第三个测试用例，夹具返回值 --- ')

if __name__ == '__main__':
    pytest.main(['-k','test_fixture'])