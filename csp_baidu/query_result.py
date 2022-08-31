# -*- coding: utf-8 -*-

import requests
import json
import sys
import os

import codecs
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

import time
timer = time.perf_counter


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#填写百度控制台中相关开通了“音频文件转写”接口的应用的的API_KEY及SECRET_KEY
dirname = os.path.abspath(os.path.dirname(__file__))
with open(dirname+'./signature.json') as json_file:
    data = json.load(json_file)

    # 读取json中的key value
    API_KEY     = data['API_KEY']
    SECRET_KEY  = data['SECRET_KEY']

"""  获取请求TOKEN start 通过开通音频文件转写接口的百度应用的API_KEY及SECRET_KEY获取请求token"""
TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'

'''
选择能力域
'''
# SCOPE = 'brain_bicc'  # 有此scope表示有asr能力，没有请在网页里勾选 bicc
SCOPE = 'brain_asr_async'  # 有此scope表示有asr能力，没有请在网页里勾选
# SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里勾选

class DemoError(Exception):
    pass

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()

    result_str =  result_str.decode()

#    print(result_str)
    result = json.loads(result_str)
#    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
#        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  获取鉴权结束，TOKEN end """

"""  发送查询结果请求 """

'''
根据参数个数，验证脚本运行时的参数
'''
if len(sys.argv) != 3:
    # 参数1：当前脚本
    # 参数2：任务id文本
    # 参数3：输出目录
    sys.stderr.write("this_py_name.py <task_id_output> <OUTPUT_DIR>\n")
    exit(-1)

# 读取 链接文本文档 的内容
OPT         = sys.argv[1]
DIR         = sys.argv[2]

task_id         = codecs.open(OPT, 'r',  'utf8')

task_id_list = []
fileName_list = []
for each in task_id:
    each = each.strip()
    fileName,taskId = each.split('\t')
    task_id_list.append(taskId)
    fileName_list.append(fileName)

task_id.close()

hyp_output = codecs.open(DIR+'/HYP.txt', 'w+', 'utf8')
ref_output = codecs.open(DIR+'/REF.txt', 'w+', 'utf8')
temp_json = codecs.open(DIR+'HYP.json', 'w+', 'utf8')
temp_json.write('{"data":[')
for task in task_id_list:

    print(f'查询任务id：{task}')
    url = 'https://aip.baidubce.com/rpc/2.0/aasr/v1/query'  #查询音频任务转写结果请求地址

    body = {
        "task_ids": [task],
    }

    token = {"access_token":fetch_token()}

    headers = {'content-type': "application/json"}

    response = requests.post(url,params=token,data = json.dumps(body), headers = headers)

    # print(response.text)
    task_status = json.loads(str(json.dumps(response.json(), ensure_ascii=False)))['tasks_info'][0]['task_status']
    if task_status == 'Success':
        print(f'任务提交成功！文件 {fileName_list[task_id_list.index(task)]} 识别完毕')
        temp_json.write(json.dumps(response.json(), ensure_ascii=False) + ',')
        # print(json.dumps(response.json(), ensure_ascii=False))
        result = json.loads(str(json.dumps(response.json(), ensure_ascii=False)))['tasks_info'][0]['task_result']['result'][0]
        result = result.replace('。','')
        result = result.replace('，','')
        result = result.replace('？','')
        result = result.replace('！','')
        result = result.replace('…','')
        result = result.replace(',','')
        result = result.replace('.','')
        result = result.replace('?','')
        result = result.replace(' ','')
        hyp_output.write(fileName_list[task_id_list.index(task)] + '\t' + result + '\n')
        
    else:
        print(task_status)


temp_json.write(']}')
task_id.close()
hyp_output.close()
ref_output.close()
temp_json.close()

