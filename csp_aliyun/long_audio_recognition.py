# -*- coding: utf8 -*-
import json
import time
import sys
import os
import re
import string
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def fileTrans(akId, akSecret, appKey, fileLink) :
    # 地域ID，固定值。
    REGION_ID = "cn-shanghai"
    PRODUCT = "nls-filetrans"
    DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
    API_VERSION = "2018-08-17"
    POST_REQUEST_ACTION = "SubmitTask"
    GET_REQUEST_ACTION = "GetTaskResult"
    # 请求参数
    KEY_APP_KEY = "appkey"
    KEY_FILE_LINK = "file_link"
    KEY_VERSION = "version"
    KEY_ENABLE_WORDS = "enable_words"
    KEY_ENABLE_TIMESTAMP_ALIGNMENT = "enable_timestamp_alignment"
    KEY_FIRST_CHANNEL_ONLY = "first_channel_only"
    # 是否开启智能分轨
    KEY_AUTO_SPLIT = "auto_split"
    # 响应参数
    KEY_TASK = "Task"
    KEY_TASK_ID = "TaskId"
    KEY_STATUS_TEXT = "StatusText"
    KEY_RESULT = "Result"
    # 状态值
    STATUS_SUCCESS = "SUCCESS"
    STATUS_RUNNING = "RUNNING"
    STATUS_QUEUEING = "QUEUEING"
    
    # 创建AcsClient实例
    client = AcsClient(akId, akSecret, REGION_ID)
    # 提交录音文件识别请求
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name(POST_REQUEST_ACTION)
    postRequest.set_method('POST')
    # 新接入请使用4.0版本，已接入（默认2.0）如需维持现状，请注释掉该参数设置。

    # 设置是否输出词信息，默认为false，开启时需要设置version为4.0。
    task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False}

    # 设置是否输出词信息，默认为false，开启时需要设置version为4.0。
    # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : True, KEY_AUTO_SPLIT : True, KEY_ENABLE_TIMESTAMP_ALIGNMENT : True}

    # 开启智能分轨，如果开启智能分轨，task中设置KEY_AUTO_SPLIT为True。
    # task = {KEY_APP_KEY : appKey, KEY_FILE_LINK : fileLink, KEY_VERSION : "4.0", KEY_ENABLE_WORDS : False, KEY_AUTO_SPLIT : True}

    task = json.dumps(task)
    print(task)
    postRequest.add_body_params(KEY_TASK, task)
    taskId = ""
    try :
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        print (postResponse)
        statusText = postResponse[KEY_STATUS_TEXT]
        if statusText == STATUS_SUCCESS :
            print ("录音文件识别请求成功响应！")
            taskId = postResponse[KEY_TASK_ID]
        else :
            print ("录音文件识别请求失败！")
            return
    except ServerException as e:
        print (e)
    except ClientException as e:
        print (e)
    # 创建CommonRequest，设置任务ID。
    getRequest = CommonRequest()
    getRequest.set_domain(DOMAIN)
    getRequest.set_version(API_VERSION)
    getRequest.set_product(PRODUCT)
    getRequest.set_action_name(GET_REQUEST_ACTION)
    getRequest.set_method('GET')
    getRequest.add_query_param(KEY_TASK_ID, taskId)
    # 提交录音文件识别结果查询请求
    # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，
    # 或者为错误描述，则结束轮询。
    statusText = ""
    while True :
        try :
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            print (getResponse)
            statusText = getResponse[KEY_STATUS_TEXT]
            if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING :
                # 继续轮询
                time.sleep(10)
            else :
                # 退出轮询
                break
        except ServerException as e:
            print (e)
        except ClientException as e:
            print (e)
    if statusText == STATUS_SUCCESS :
        
        print ("录音文件识别成功！")

        '''此处是作者自定义的结果输出方式'''
        # by @沐霄
        rec_text_list = []

        # 计算
        duration = []
        rec_duration_list = []
        rec_result_list = []
        for each in getResponse['Result']['Sentences']:
            rec_text_list.append(each['Text'])
            duration = [each['BeginTime'],each['EndTime']]
            rec_duration_list.append(duration)
        rec_result_list = [list(t) for t in zip(rec_duration_list,rec_text_list)]
        '''结束'''


    else :
        print ("录音文件识别失败！")
    return rec_result_list

'''此处是作者自定义的识别文本去标点函数'''
def rm_punctuation(text:str) -> str:
    """移除标点符号"""
    PUNCTIUATION = u"[！？，、。＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏" + string.punctuation + ']+'
    rule = re.compile(PUNCTIUATION)
    text = re.sub(rule, "", text)
    return text



if __name__ == '__main__':

    try:

        if len(sys.argv) != 3:
            # 参数1：文件，当前脚本
            # 参数2：文件，存放文件链接的文本文档 | 每一行是一个 http/https 链接
            # 参数3：要输出结果的目录
            sys.stderr.write("this_py_name.py <links_file> <output_dir>\n")
            exit(-1)

        # 读取signature.json文件中的密钥
        dirname = os.path.abspath(os.path.dirname(__file__))
        with open(dirname+'./signature.json') as json_file:
            data = json.load(json_file)

            # Print the type of data variable
            accessKeyId     = data['accessKeyId']
            accessKeySecret = data['accessKeySecret']
            appKey          = data['appKey']

        # 存储参数
        LNK         = sys.argv[1]
        DIR         = sys.argv[2]
        
        # 指定存储 识别结果文本 的文件
        hyp_output = open(DIR+'./HYP.txt', 'w', encoding='utf8')

        # 读取指定参数（第2个参数）对应的文本，文本中的链接文件必须同属于同一个数据集。
        links = open(LNK, 'r',  encoding='utf8')
        
        for l in links:
            # 清理
            l = l.strip()

            # 链接存为 fileLink
            fileLink = l

            # 解析链接中的文件名
            fileName = l.split('/')[-1]

            # 构建一个 hyp_list
            hyp_list = []

            # # 执行录音文件识别，把结果中的 时间值、文本值 提取到 hyp_list
            hyp_list = fileTrans(accessKeyId, accessKeySecret, appKey, fileLink)

            rec_text = ''
            for each in hyp_list:
                each[1] = rm_punctuation(each[1])
                rec_text += each[1]

            hyp_output.write(fileName + '\t' + rec_text + '\n')
            hyp_output.flush()
            
            
        hyp_output.close()
        links.close()
    
    except:
        
        # 报错处理，请自定义
        pass