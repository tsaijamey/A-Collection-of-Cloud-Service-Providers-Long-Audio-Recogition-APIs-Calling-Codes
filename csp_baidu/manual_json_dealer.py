import sys,codecs,json

if len(sys.argv) != 4:
    # 参数1：当前脚本
    # 参数2：链接文本文档
    # 参数3：HYP 的结果输出文本
    sys.stderr.write("this_py_name.py <task_id_output> <json_file> <HYP.txt>\n")
    exit(-1)

OPT         = sys.argv[1]
JSN         = sys.argv[2]
HYP         = sys.argv[3]

task_id = codecs.open(OPT, 'r',  'utf8')
task_id_list = []
fileName_list = []
for each in task_id:
    each = each.strip()
    fileName,taskId = each.split('\t')
    task_id_list.append(taskId)
    fileName_list.append(fileName)

task_id.close()

json_file = codecs.open(JSN, 'r', 'utf8')
json_data = json.load(json_file)['data']   

hyp_output = codecs.open(HYP, 'w+', 'utf8')
for each in task_id_list:
    result = json_data[task_id_list.index(each)]['tasks_info'][0]['task_result']['result'][0]
    result = result.replace('。','')
    result = result.replace('，','')
    result = result.replace('？','')
    result = result.replace('！','')
    result = result.replace('…','')
    result = result.replace(',','')
    result = result.replace('.','')
    result = result.replace('?','')
    result = result.replace(' ','')
    hyp_output.write(fileName_list[task_id_list.index(each)] + '\t' + result + '\n')


json_file.close()
hyp_output.close()