import time
from datetime import timedelta
import pytest
import os
import threading
from collections import defaultdict
from unit_tools.handle_data.yaml_handler import clear_yaml
from unit_tools.other_util.ding_rebot import send_dd_msg
from config.setting import is_dd_msg


@pytest.fixture(scope="session",autouse=True)
def clear_extract():
    clear_yaml()


# 使用线程安全的字典存储统计信息
worker_stats = defaultdict(lambda: {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'error': 0
})

# 线程锁用于保证统计的线程安全
_stats_lock = threading.Lock()


def pytest_sessionstart(session):
    """在测试会话开始时记录时间"""
    # 将开始时间存储在 session.config 中
    session.config.session_start_time = time.time()

def get_worker_id():
    """获取当前工作节点ID"""
    try:
        # 方法1: 通过环境变量获取 (xdist方式)
        worker_id = os.environ.get('PYTEST_XDIST_WORKER')
        if worker_id:
            return worker_id

        # 方法2: 通过pytest config获取
        if hasattr(pytest, 'config') and pytest.config:
            config = pytest.config
            if hasattr(config, 'workerinput') and config.workerinput:
                return config.workerinput.get('workerid', 'master')

        # 方法3: 通过请求配置获取
        import _pytest.config
        config = _pytest.config.Config._instance
        if config and hasattr(config, 'workerinput') and config.workerinput:
            return config.workerinput.get('workerid', 'master')

    except Exception:
        pass

    return 'master'



@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """收集测试用例执行结果"""
    outcome = yield
    report = outcome.get_result()

    # 确保只在测试用例执行阶段统计
    if report.when == "call":
        worker_id = get_worker_id()

        with _stats_lock:
            worker_stats[worker_id]['total'] += 1

            if report.passed:
                if hasattr(report, 'wasxfail'):
                    worker_stats[worker_id]['passed'] += 1
                else:
                    worker_stats[worker_id]['passed'] += 1
            elif report.failed:
                worker_stats[worker_id]['failed'] += 1
            elif report.skipped:
                worker_stats[worker_id]['skipped'] += 1


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """在终端显示统计摘要"""
    worker_id = get_worker_id()

    # 只在主进程中显示统计
    if worker_id != 'master':
        return


    # 从terminalreporter获取统计信息作为备选
    terminal_stats = {
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        'error': len(terminalreporter.stats.get('error', [])),
    }
    terminal_total = sum(terminal_stats.values())
    pass_num = terminal_stats['passed']
    fail_num = terminal_stats['failed']
    skip_num = terminal_stats['skipped']
    error_num = terminal_stats['error']
    duration = 0
    session_start_time = getattr(config, 'session_start_time', None)
    if session_start_time:
        duration = round(time.time() - session_start_time, 2)
    formatted_duration = str(timedelta(seconds=duration)).split('.')[0]


    pass_rate = f'{(pass_num / terminal_total)* 100:.2f}%' if terminal_total > 0 else "N/A"
    fail_rate = f'{(fail_num / terminal_total)* 100:.2f}%' if terminal_total > 0 else "N/A"
    error_rate = f'{(error_num / terminal_total)* 100:.2f}%' if terminal_total > 0 else "N/A"
    summary = f"""
    UI自动化测试结果，通知如下，具体执行结果：
    测试用例总数量：{terminal_total}
    测试用例通过数量：{pass_num}
    通过率：{pass_rate}
    测试用例失败数量：{fail_num}
    失败率：{fail_rate}
    测试用例错误数量：{error_num}
    错误率：{error_rate}
    测试用例跳过数量：{skip_num}
    执行总时长：{formatted_duration}
    """
    if is_dd_msg:
        send_dd_msg(summary)

