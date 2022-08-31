#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import codecs
import os

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
timer = time.perf_counter


import ssl
ssl._create_default_https_context = ssl._create_unverified_context




'''
Section Description:

    读取API_KEY和SECRET_KEY
'''
#填写百度控制台中相关开通了“音频文件转写”接口的应用的的API_KEY及SECRET_KEY
dirname = os.path.abspath(os.path.dirname(__file__))
with open(dirname+'./signature.json') as json_file:
    data = json.load(json_file)

    # 读取json中的key value
    API_KEY     = data['API_KEY']
    SECRET_KEY  = data['SECRET_KEY']




'''
Section Description:

    获取请求TOKEN start
    通过开通音频文件转写接口的百度应用的API_KEY及SECRET_KEY获取请求token
'''
class DemoError(Exception):
    pass

TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
# SCOPE = 'brain_bicc'  # 有此scope表示有asr能力，没有请在网页里勾选 bicc
SCOPE = 'brain_asr_async'  # 有此scope表示有asr能力，没有请在网页里勾选
# SCOPE = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里勾选

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode( 'utf-8')
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




"""  发送识别请求 """

#待进行语音识别的音频文件url地址，需要可公开访问。
if len(sys.argv) != 3:
    # 参数1：当前脚本
    # 参数2：链接文本文档
    # 参数3：task_id的输出文本
    sys.stderr.write("this_py_name.py <links_file> <task_id_output>\n")
    exit(-1)

# 读取 链接文本文档 的内容
LNK         = sys.argv[1]
OPT         = sys.argv[2]

links = codecs.open(LNK, 'r',  'utf8')
speech_url_list = []
fileName_list = []
for each in links:
    each = each.strip()
    speech_url_list.append(each)
    fileName_list.append(each.split('/')[-1])

links.close()

task_id_output = codecs.open(OPT, 'w+', 'utf8')
for speech_url in speech_url_list:


    url = 'https://aip.baidubce.com/rpc/2.0/aasr/v1/create'  #创建音频转写任务请求地址

    body = {
        "speech_url": speech_url,
        "format": "pcm",        #音频格式，支持pcm,wav,mp3，音频格式转化可通过开源ffmpeg工具（https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf）或音频处理软件
        "pid": 1537,        #模型pid，1537为普通话输入法模型，1737为英语模型
        "rate": 16000       #音频采样率，支持16000采样率，音频格式转化可通过开源ffmpeg工具（https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf）或音频处理软件
        # "pid": 1134,        #模型pid，1134为呼叫中心中文普通话模型
        # "rate": 8000       #音频采样率，支持8k采样率，音频格式转化可通过开源ffmpeg工具（https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf）或音频处理软件
    }

    # token = {"access_token":"24.19fd462ac988cb2d1cdef56fcb4b568a.2592000.1579244003.282335-11778379"}

    token = {"access_token":fetch_token()}

    headers = {'content-type': "application/json"}

    response = requests.post(url,params=token,data = json.dumps(body), headers = headers)

    # 返回请求结果信息，获得task_id，通过识别结果查询接口，获取识别结果
    # print(response.text)

    # 返回响应头
    # print(response.status_code)

    # print(token)

    # 记录返回的 task_id
    print(response.text)
    task_status = json.loads(response.text)['task_status']
    print(task_status)
    task_id = json.loads(response.text)['task_id']
    if task_status == 'Created':
        task_id_output.write(fileName_list[speech_url_list.index(speech_url)] + '\t' + task_id + '\n')
        print(f'任务提交成功！文件 {fileName_list[speech_url_list.index(speech_url)]} 的task_id为：{task_id}')
    
task_id_output.close()


