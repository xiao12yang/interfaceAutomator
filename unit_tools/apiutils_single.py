"""
处理单接口
"""
import copy
import json
import re
import traceback
from json import JSONDecodeError

import allure
import jsonpath

from unit_tools.debugtalk import DebugTalk
from unit_tools.handle_data.yaml_handler import read_yaml, write_yaml
from unit_tools.handle_data.configParse import ConfigParser
from unit_tools.sendrequests import SendRequest
from unit_tools.assertion_utils import Assertions
from unit_tools.log_util.recordlog import logs


class RequestsBase:
    def __init__(self):
        self.config = ConfigParser()
        self.send_request = SendRequest()
        self.asserts = Assertions()

    @classmethod
    def parses_replace_variables(cls, yaml_data):
        """
        解析并替换yaml数据中的变量引用
        :param yaml_data: 解析的yaml数据
        :return: 返回dict类型
        """
        yaml_data_str = yaml_data if isinstance(yaml_data, str) else json.dumps(yaml_data, ensure_ascii=False)
        for _ in range(yaml_data_str.count('${')):
            if '${' in yaml_data_str and '}' in yaml_data_str:
                start_index = yaml_data_str.index('${')
                end_index = yaml_data_str.index('}', start_index)
                variable_data = yaml_data_str[start_index:end_index + 1]
                # 使用正则表达式提取函数名
                match = re.match(r'\$\{(\w+)\((.*?)\)\}', variable_data)
                if match:
                    func_name = match.group(1)
                    func_params = match.group(2)
                    func_params = func_params.split(',') if func_params else []
                    # 面向对象反射getattr调用函数
                    extract_data = getattr(DebugTalk(), func_name)(*func_params)

                    # 使用正则表达式替换原始字符中的变量引用为调用后结果
                    # 在 yaml_data_str 字符串中，将所有匹配 variable_data 的内容替换为 str(extract_data)
                    yaml_data_str = re.sub(re.escape(variable_data), str(extract_data), yaml_data_str)

        # 还原数据，将其转换成字典类型
        try:
            data = json.loads(yaml_data_str)
        except json.JSONDecodeError as e:
            data = yaml_data_str
        return data

    @classmethod
    def allure_attach_dict_response(cls, result):
        """
        处理结果是字典类型，就转换成字符串类型，并做格式化处理，否则直接返回
        :return:
        """
        if isinstance(result, dict):
            allure_response = json.dumps(result, ensure_ascii=False, indent=4)
        else:
            allure_response = result
        return allure_response

    def execute_test_case(self, base_info, test_case):
        """
        规范yaml接口信息、执行接口、提取结果、断言操作
        :param base_info: 接口信息
        :param test_case_s: 测试用例
        :return:
        """
        try:
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称：{api_name}', attachment_type=allure.attachment_type.TEXT)

            url = self.config.get_host('host') + base_info['url']
            allure.attach(url,f'接口地址：{url}',attachment_type=allure.attachment_type.TEXT)

            method = base_info['method']
            allure.attach(method, f'请求方式：{method}', attachment_type=allure.attachment_type.TEXT)

            headers = base_info.get('headers')
            if headers is not None:
                headers = eval(self.parses_replace_variables(headers)) if isinstance(headers, str) else headers
            allure.attach(json.dumps(headers), f'请求头：{headers}', attachment_type=allure.attachment_type.TEXT)

            cookies = base_info.get('cookies')
            if cookies is not None:
                cookies = eval(self.parses_replace_variables(cookies)) if isinstance(cookies, str) else cookies
            allure.attach(json.dumps(cookies), f'Cookie：{cookies}', attachment_type=allure.attachment_type.TEXT)

            test_case_s = copy.deepcopy(test_case)
            case_name = test_case_s.pop('case_name')
            allure.attach(case_name, f'测试用例名称：{case_name}', attachment_type=allure.attachment_type.TEXT)

            # 通过变量引处理断言结果
            validation = self.parses_replace_variables(test_case_s.get('validation'))
            test_case_s.pop('validation')

            # 处理接口返回值提取部分
            extract = test_case_s.pop('extract', None)
            extract_list = test_case_s.pop('extract_list', None)

            # 处理参数类型和请求参数
            for param_type, param_value in test_case_s.items():
                if param_type in ['data', 'params', 'json']:
                    test_case_s[param_type] = self.parses_replace_variables(param_value)
                    allure.attach(f'参数类型：{param_type}\n{self.allure_attach_dict_response(test_case_s[param_type])}', f'参数类型：{param_type}', attachment_type=allure.attachment_type.TEXT)


            # 处理文件上传
            files = test_case_s.pop('files', None)
            if files:
                for fk,fv in files.items():
                    files = {fk:open(fv,'rb')}

            response = self.send_request.execute_api_request(api_name=api_name, url=url, method=method,
                                                             headers=headers, case_name=case_name, cookies=cookies,
                                                             files=files, **test_case_s)
            allure.attach(self.allure_attach_dict_response(response.json()), "接口实际返回信息",
                              attachment_type=allure.attachment_type.TEXT)

            status_code = response.status_code
            response_text = response.text

            # 可能携带换行符，影响美观，所有稍微处理一下
            response_log = response_text.replace('\n', '').replace('\r', '').strip()
            logs.info(f'实际接口返回结果{response_log}')

            # 处理接口返回值提取
            if extract is not None:
                self.extract_data(extract,response_text)
            if extract_list is not None:
                self.extract_data_list(extract_list,response_text)

            # 处理接口断言
            self.asserts.assert_result(validation,response.json(),status_code)
        except Exception as e:
            logs.error(f'出现未知异常 -- {str(traceback.format_exc())}')
            raise e

    @classmethod
    def extract_data(cls,testcase_extract,response_text):
        """
        提取单个参数，提取接口的返回参数，支持正则表达式和json提取器，
        :param testcase_extract: dict字典类型，yaml文件中的extract值，例如：{'token': '$.token'}
        :param response_text: (str)接口的实际返回值
        :return:
        """
        extract_data = None
        try:
            for key,value in testcase_extract.items():
                if any(pat in value for pat in ['(.*?)','(.+?)',r'(\d+)',r'(\d*)']):
                    ext_match = re.search(value,response_text)
                    if ext_match:
                        extract_data = {key:int(ext_match.group(1)) if (r'\d+') in value else ext_match.group(1)}
                    else:
                        extract_data = {key:'未提前到关键数据'}
                elif "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response_text),value)[0]
                    extract_data = {key:ext_json} if ext_json else {key:'未提取到数据，请检查返回信息或表达式!'}
                if extract_data:
                    write_yaml(extract_data)
        except re.error as e:
            logs.error('正则表达式或jsonpath解析错误，请检查yaml文件extract表达式是否正确')
        except JSONDecodeError as e:
            logs.error('JSON解析错误，请检查yaml文件extract表达式是否正确')
    @classmethod
    def extract_data_list(cls, testcase_extract_list,response_text):
        """
        提取多个参数，提取接口的返回参数，支持正则表达式和json提取器
        :param testcase_extract_list: dict字典类型，yaml文件中的extract_list值，例如：{'good_ids': '$.good_ids'}
        :param response_text: (str)接口的实际返回值
        :return:
        """
        extract_data_list = None
        try:
            for key,value in testcase_extract_list.items():
                if any(pat in value for pat in ['(.*?)','(.+?)',r'(\d+)',r'(\d*)']):
                    ext_list = re.findall(value,response_text,re.S)
                    if ext_list:
                        extract_data_list = {key:ext_list}
                elif "$" in value:
                    ext_list = jsonpath.jsonpath(json.loads(response_text),value)
                    if ext_list:
                        extract_data_list = {key:ext_list}
                    else:
                        extract_data_list = {key: '未提取到数据，请检查返回信息或表达式!'}
                if extract_data_list:
                    write_yaml(extract_data_list)
        except re.error as e:
            logs.error('正则表达式或jsonpath解析错误，请检查yaml文件extract表达式是否正确')
        except JSONDecodeError as e:
            logs.error('JSON解析错误，请检查yaml文件extract表达式是否正确')

if __name__ == '__main__':
    data = read_yaml('../data/login.yaml')
    req = RequestsBase()
    data = req.parses_replace_variables(data)
    # req.execute_test_case(data[0],data[1])
