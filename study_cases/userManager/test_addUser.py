import pytest
class TestAddUser:
    @pytest.mark.P1
    def test_add_user_001(self):
        print('添加用户成功1')

    # @pytest.mark.first
    def test_add_user_002(self):
        print('添加用户成功2')

    # @pytest.mark.last
    def test_add_user_003(self):
        print('添加用户成功3')



if __name__ == '__main__':
    pytest.main(["-s"])