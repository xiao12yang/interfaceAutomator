
from requests import utils
import requests

url_login = 'http://127.0.0.1:8787/dar/user/login'
data_login = {
    "user_name": "test01",
    "passwd": "admin123"
}
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
res = requests.request('POST',url_login,headers=headers,data=data_login)

# 获取接口的cookie信息，一般都是通过登录接口
print(res.cookies)
# 获取cookie，以字典的类型返回
cookie = requests.utils.dict_from_cookiejar(res.cookies)


# 后续接口中使用cookie信息来验证登录状态
url = 'http://127.0.0.1:8787/api/order/customer/orderPlan/getMaterial'
headers = {'Content-Type': 'application/json',
           'charset': 'UTF-8'
           }

res = requests.request('GET',url,headers=headers,cookies=cookie)
print(res.text)

# session = requests.Session()
# res = session.request('POST', url_login, headers=headers, data=data_login)
# print(res.text)
