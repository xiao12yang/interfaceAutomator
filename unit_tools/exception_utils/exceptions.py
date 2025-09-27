class AssertTypeError(Exception):
    """
    yaml文件断言模式类型作物异常
    """
    def __init__(self,message='不支持该模式断言'):
        self.message = message
