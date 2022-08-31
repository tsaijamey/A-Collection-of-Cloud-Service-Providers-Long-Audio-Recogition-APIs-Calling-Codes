# 官方文档代码
# encoding:utf-8
# client_id 对应的是AK，client_secret 对应的是SK，均从 控制台>应用列表中查看对应的应用详情 获得。
import requests

# 填写网页上申请的appkey 如 API_KEY="g8eBUMSokVB1BHGmgxxxxxx"
API_KEY = 'hT3a2ePLsL2ZIcTr5y61BGXH'

# 填写网页上申请的APP SECRET 如 SECRET_KEY="94dc99566550d87f8fa8ece112xxxxx"
SECRET_KEY = 'cBGyEi32ZRVXbOt5Y4xvXXsyjMLSqmqU'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY
response = requests.get(host)
# if response:
#     print(response.json())


# 个人代码
# 目标：从json中，解析access_token
import json

json_str=json.dumps(response.json())
# print(f'json_str为：{json_str}')
# print(type(json_str))

# #将JSON数据解码为dict
data1=json.loads(json_str)

if response:
    print(data1['access_token'])
# print(type(data1))