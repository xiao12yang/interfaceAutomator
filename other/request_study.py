import json
import requests

# 发送get请求
url = 'http://127.0.0.1:8787/coupApply/cms/goodsList'
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
req_data = {
    "msgType": "getHandsetListOfCust",
    "page": 1,
    "size": 20
}

response = requests.request('GET', url, headers=headers, params=req_data)

# 响应结果默认返回接口的状态码
print(response.status_code)
# 获取接口响应内容（文本）
print(response.text)
# 获取接口响应内容（json）
print(response.json())

url_login = 'http://127.0.0.1:8787/dar/user/login'
data_login = {
    "user_name": "test01",
    "passwd": "admin123"
}
# post请求
res_post = requests.request('POST', url_login, headers=headers, data=data_login)
print(res_post.status_code)
print(res_post.text)
print(res_post.json())
# 如果接口返回信息出现转义编码时，返回的是Unicode，要手动转换
print(res_post.text.encode().decode('utf-8')) # encode()编码，decode()解码


# post请求的json提交数据
url = 'http://127.0.0.1:8787/coupApply/cms/productDetail'
headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
data_json = {
    "pro_id": "33809635011",
    "page": 1,
    "size": 20
}
res = requests.request('POST',url,headers=headers,json=data_json)
print(res.status_code)
print(res.text)
print(res.json())



print('*'*20,'session')
# 会话（session）对象，使用会话对象可以在多个请求之间保持状态，假如保持登录状态
# 创建一个会话
session = requests.Session()
headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
res = session.request('POST',url_login,headers=headers,data=data_login)
print(res.text)
# res2 = session.request('')