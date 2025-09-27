import time
from datetime import timedelta
import pytest

from unit_tools.handle_data.yaml_handler import clear_yaml
from unit_tools.other_util.ding_rebot import send_dd_msg
from config.setting import is_dd_msg


@pytest.fixture(scope="session",autouse=True)
def clear_extract():
    clear_yaml()


def pytest_sessionstart(session):
    """在测试会话开始时记录时间"""
    # 将开始时间存储在 session.config 中
    session.config.session_start_time = time.time()



def pytest_terminal_summary(terminalreporter,exitstatus,config):
    """
    Pytest框架里面预定义的钩子函数，用于在测试结束后自动化收集测试结果
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """
    # print(terminalreporter.stats)
    testcase_total = terminalreporter._numcollected
    passed_num = len(terminalreporter.stats.get("passed",[]))
    failed_num = len(terminalreporter.stats.get("failed",[]))
    error_num = len(terminalreporter.stats.get("error",[]))
    skipped_num = len(terminalreporter.stats.get("skipped",[]))
    duration = 0
    session_start_time = getattr(config, 'session_start_time', None)
    if session_start_time:
        duration = round(time.time() - session_start_time,2)
    formatted_duration = str(timedelta(seconds=duration)).split('.')[0]

    # 统计通过率、失败率、错误率
    pass_rate = f'{(passed_num/testcase_total)*100:.2f}%' if testcase_total > 0 else "N/A"
    fail_rate = f'{(failed_num/testcase_total)*100:.2f}%' if testcase_total > 0 else "N/A"
    error_rate = f'{(error_num/testcase_total)*100:.2f}%' if testcase_total > 0 else "N/A"



    summary = f"""
    自动化测试结果，通知如下，具体执行结果：
    测试用例总数量：{testcase_total}
    测试用例通过数量：{passed_num}   
    通过率：{pass_rate}
    测试用例失败数量：{failed_num}   
    失败率：{fail_rate}
    测试用例错误数量：{error_num}    
    错误率：{error_rate}
    测试用例跳过数量：{skipped_num}
    执行总时长：{formatted_duration}
    """
    if is_dd_msg:
        send_dd_msg(summary)

