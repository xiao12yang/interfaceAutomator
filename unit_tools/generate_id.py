"""
生成器
"""
def generate_module_id():
    """
    生成模块id
    :return:
    """
    for i in range(1,1000):
        module_id = 'M'+str(i).zfill(2)+'_'
        yield module_id

def generate_testcase_id():
    """
    生成测试用例编号
    :return:
    """
    for i in range(1,10000):
        testcase_id = 'T'+str(i).zfill(2)+'_'
        yield testcase_id

m_id = generate_module_id()
t_id = generate_testcase_id()