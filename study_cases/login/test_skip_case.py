import pytest

class TestSkipCase:
    @pytest.mark.skip
    def test_skip_case_001(self):
        print('被跳过')

    def test_skip_case_002(self):
        print('没有被跳过')
    @pytest.mark.skipif(condition=True,reason='符合条件被跳过')
    def test_skip_case_003(self):
        print('符合条件被跳过')
    @pytest.mark.skipif(condition=False,reason='不符合跳过条件')
    def test_skip_case_004(self):
        print('不符合跳过条件，没被跳过')

    @pytest.mark.xfail
    def test_skip_case_005(self):
        print('预期失败')


if __name__ == '__main__':
    pytest.main()