import pytest

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    print('测试函数执行前执行的前置操作')
    yield
    print('测试函数执行后执行的后置操作')


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown1():
    print('模块.py执行前')
    yield
    print('模块.py执行后')
