from typing import Callable, Any

import allure
import jsonpath

from unit_tools.exception_utils.exceptions import AssertTypeError
from unit_tools.db_connector.connectMysql import ConnectMysql
from unit_tools.log_util.recordlog import logs

class Assertions:
    """
    接口断言模式封装
    1）状态码断言
    2）包含模式断言
    3）相等断言
    4）不相等断言
    5）数据库断言
    """

    @classmethod
    def status_code_assert(cls, expected_result, status_code_):
        """
        接口的响应状态码断言模式
        :param expected_result: yaml文件code模式的预期状态码
        :param status_code: 接口实际返回的状态码
        :return:
        """
        # 断言状态标识，0表示成功，其他表示失败
        failure_count = 0
        status_code = status_code_ if isinstance(status_code_, int) else int(status_code_)
        if expected_result == status_code:
            logs.info(f'状态码断言成功：接口实际返回状态码：{status_code} == {expected_result}')
            allure.attach(f"预期结果：{str(status_code)}\n实际结果：{str(expected_result)}", '状态码断言：成功',
                          attachment_type=allure.attachment_type.TEXT)
        else:
            logs.error(f'状态码断言失败：接口实际返回状态码：{status_code} != {expected_result}')
            allure.attach(f"预期结果：{str(status_code)}\n实际结果：{str(expected_result)}", '状态码断言：失败',
                          attachment_type=allure.attachment_type.TEXT)
            failure_count += 1
        return failure_count

    @classmethod
    def contain_assert(cls, expected_result, response_result):
        """
        字符串包含模式，断言预期结果字符串是否包含在接口的实际响应信息中
        :param expected_result: dict yaml文件contain模式的预期数据
        :param response_result: dict 接口实际响应信息
        :return:
        """
        failure_count = 0
        response_str = None
        for assert_key, assert_value in expected_result.items():
            response_list = jsonpath.jsonpath(response_result, f'$..{assert_key}')
            if response_list and isinstance(response_list[0], str):
                response_str = ''.join(response_list)
                if assert_value in response_str:
                    logs.info(f'包含模式断言成功：预期结果【{assert_value}】存在于实际结果【{response_str}】中')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '字符串包含断言：成功',
                                  attachment_type=allure.attachment_type.TEXT)
                else:
                    logs.error(f'包含模式断言失败：预期结果【{assert_value}】不存在于实际结果【{response_str}】中')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '字符串包含断言：失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
            else:
                logs.error(
                    f'包含模式断言失败，预期结果【{assert_key}:{assert_value}】不存在于实际结果中，请检查预期结果或接口返回值是否正确')
                allure.attach(f"预期结果：{assert_key}:{assert_value}不存在于实际结果中", '字符串包含断言：失败',
                              attachment_type=allure.attachment_type.TEXT)
                failure_count += 1
        return failure_count

    @classmethod
    def equal_assert(cls, expected_result, response_result):
        """
        相等断言，根据yaml文件中的validation下的eq模式数据跟接口实际响应数据对比
        :param expected_result: dict yaml中的eq值，即预期结果
        :param response_result: dict 接口响应返回值，即实际结果
        :return:
        """
        failure_count = 0

        if isinstance(expected_result, dict) and isinstance(response_result, dict):
            for assert_key, assert_value in expected_result.items():
                response_str = response_result.get(assert_key)
                if assert_value == response_str and response_str is not None:
                    logs.info(
                        f'相等模式断言成功，预期结果【{assert_key}:{assert_value}】 == 实际结果【{assert_key}:{response_str}】')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '相等断言：成功',
                                  attachment_type=allure.attachment_type.TEXT)
                elif response_result.get(assert_key) is None:
                    logs.error(
                        f'相等模式断言失败，预期结果【{assert_key}:{assert_value}】不存在于实际结果中，请检查预期结果或接口返回值是否正确')
                    allure.attach(f"预期结果：{assert_key}:{assert_value}不存在于实际结果中", '相等断言：失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
                else:
                    logs.error(
                        f'相等模式断言失败，预期结果【{assert_key}:{assert_value}】 != 实际结果【{assert_key}:{response_result.get(assert_key)}】')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '相等断言：失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
        return failure_count

    @classmethod
    def not_equal_assert(cls, expected_result, response_result):
        """
        相等断言，根据yaml文件中的validation下的eq模式数据跟接口实际响应数据对比
        :param expected_result: dict yaml中的eq值，即预期结果
        :param response_result: dict 接口响应返回值，即实际结果
        :return:
        """
        failure_count = 0
        if isinstance(expected_result, dict) and isinstance(response_result, dict):
            for assert_key, assert_value in expected_result.items():
                response_str = response_result.get(assert_key)
                if assert_value != response_str and response_str is not None:
                    logs.info(
                        f'不相等模式断言成功，预期结果【{assert_key}:{assert_value}】 != 实际结果【{assert_key}:{response_str}】')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '不相等断言：成功',
                                  attachment_type=allure.attachment_type.TEXT)
                elif response_str is None:
                    logs.error(
                        f'不相等模式断言失败，预期结果【{assert_key}:{assert_value}】不存在于实际结果中，请检查预期结果或接口返回值是否正确')
                    allure.attach(f"预期结果：{assert_key}:{assert_value}不存在于实际结果中", '不相等断言：失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
                else:
                    logs.error(
                        f'不相等模式断言失败，预期结果【{assert_key}:{assert_value}】 == 实际结果【{assert_key}:{response_str}】')
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{response_str}", '不相等断言：失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    failure_count += 1
        return failure_count

    @classmethod
    def database_assert(cls, expected_result, status_code=None):
        """
        数据库断言
        :param expected_result: yaml文件db模式中的SQL语句预期结果
        :return:
        """
        failure_count = 0
        connect = ConnectMysql()
        db_value = connect.query(expected_result)
        if db_value is not None:
            logs.info(f'数据库断言成功，db_value:{db_value}')
            allure.attach(f"SQL语句：{expected_result}\n实际结果：{db_value}", '数据库断言：成功',
                          attachment_type=allure.attachment_type.TEXT)
        else:
            failure_count += 1
            allure.attach(f"SQL语句：{expected_result}\n实际结果：{db_value}", '数据库断言：失败',
                          attachment_type=allure.attachment_type.TEXT)
            logs.error(f'数据库断言失败，请检查数据库是否存在该数据')
        return failure_count

    @classmethod
    def assert_result(cls, expected_result, response, status_code):
        """
        断言主函数，通过all_flag == 0 表示测试成功，否则失败
        :param expected_result: （list）yaml文件validation关键词下的预期结果
        :param response: (dict)接口的实际响应信息
        :param status_code: 接口的实际响应状态码
        :return:
        """
        all_flag = 0
        assert_methods = {
            'code': cls.status_code_assert,
            'contain': cls.contain_assert,
            'eq': cls.equal_assert,
            'ne': cls.not_equal_assert,
            'db': cls.database_assert,
        }
        try:
            for yq in expected_result:
                for assert_mode, assert_value in yq.items():
                    assert_method: Callable[[Any, Any], int] = assert_methods.get(assert_mode)
                    if assert_mode:
                        if assert_mode in ['code', 'db']:
                            flag = assert_method(assert_value, status_code)
                        else:
                            flag = assert_method(assert_value, response)
                        all_flag += flag
                    else:
                        logs.error(f'不支持该{assert_mode}断言模式')
                        # raise AssertionError(f'不支持该{assert_mode}断言模式')

        except Exception as e:
            logs.error(f"断言发生未知异常，原因：{e}")
        try:
            assert all_flag == 0, '测试失败'
            logs.info('测试成功')
        except Exception as e:
            logs.error(e)
            raise e
