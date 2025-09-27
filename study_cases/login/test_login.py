import random
import pytest


class TestLogin:
    @pytest.mark.P1
    def test_login_success(self):
        print('登录成功')
        assert random.choice([True, False]),'测试失败'

    # @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.skip
    def test_login_failed(self):
        print('登录失败')
        assert 1 == 2 , "断言失败，1不等于2"
    @pytest.mark.P3
    def test_login_error(self):
        print('登录错误')
        assert 1 == 1,"断言失败，1不等于1"
