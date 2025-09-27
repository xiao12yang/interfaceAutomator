import pytest


class TestSetupTeardown:

    @classmethod
    def setup_class(cls):
        print('测试类开始前执行的操作')

    @classmethod
    def teardown_class(cls):
        print("测试类结束后执行的操作")

    def setup_method(self):
        print("所有测试执行前执行的操作")
    def teardown_method(self):
        print("所有测试执行后执行的操作")

    def test_case_001(self):
        print('这是第一个测试用例')

    def test_case_002(self):
        print('这是第二个测试用例')

    def test_case_003(self):
        print('这是第三个测试用例')


if __name__ == '__main__':
    pytest.main(['-k','test_setup_teardown'])