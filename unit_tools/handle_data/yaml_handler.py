import os
import yaml
from config.setting import FILE_PATH
from unit_tools.log_util.recordlog import logs


def read_yaml(yaml_path):
    """
    读取yaml文件数据
    :param yaml_path: 文件路径
    :return:
    """
    try:
        testCases_list = []
        with open(yaml_path,'r',encoding='utf-8') as file:
            data = yaml.safe_load(file)
            if len(data) <= 1:
                yaml_data = data[0]
                base_info = yaml_data.get('baseInfo')
                for ts in yaml_data.get('testCases'):
                    testCases_list.append([base_info,ts])
                return testCases_list
            else:
                print(data)
                # for bs in data:
                #     base_info = bs.get('baseInfo')
                #     for ts in base_info.get('testCases'):
                #         testCases_list.append()
                return data
    except UnicodeDecodeError as e:
        logs.error(f'{yaml_path}文件编码格式错误，--尝试使用utf-8去解码YAML文件发生错误，请确保你的yaml文件是utf-8格式!')
    except Exception as e:
        logs.error(f'读取{yaml_path}文件时出现异常，原因：{e}')

def write_yaml(value):
    """
    yaml文件数据写入
    :param value: 数据，必须时字典类型
    :return:
    """
    file_path = FILE_PATH['extract']
    file = None
    if not os.path.exists(file_path):
        with open(file_path,'w',encoding='utf-8'):
            pass
    try:
        file = open(file_path,'a',encoding='utf-8')
        if isinstance(value,dict):
            write_data = yaml.dump(value,allow_unicode=True,sort_keys=False)
            file.write(write_data)
        else:
            logs.warning('写入的数据必须为字典类型')
    except Exception as e:
        logs.error(f'写入yaml文件出现异常，原因：{e}')
    finally:
        file.close()



def clear_yaml():
    """
    清空extract文件
    :return:
    """
    try:
        with open(FILE_PATH['extract'],'w',encoding='utf-8') as file:
            file.write("")
    except Exception as e:
        logs.error(f'清空extract文件出现异常，原因：{e}')


def get_extract_yaml(node_name,sub_node_name=None):
    """
    用来获取extract.yaml文件中的数据
    :param node_name: 第一级key值
    :param sub_node_name: 下级key值
    :return:
    """
    file_path = FILE_PATH['extract']
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            data = yaml.safe_load(file)
            # print(data)
            if sub_node_name is None:
                return data[node_name]
            else:
                return data.get(node_name,{}).get(sub_node_name)
    except yaml.YAMLError as e:
        logs.error(f'读取yaml文件失败，请检查格式 - {file_path}，{e}')
    except Exception as e:
        logs.error(f'未知异常，原因：{e}')



if __name__ == '__main__':
    res = read_yaml('../../data/productScenario.yaml')
    print(type(res))
    for item in res:
        print(item)
    print(len(res))
