#!/usr/bin/env python
# coding: utf-8
'''
用于中、英文或者中英文识别字错误率计算
'''

import os,sys
import re
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="""sclite compute error rate tool""")
    parser.add_argument('--ref', type=str, required=True, default='',
                        help='reference text')
    parser.add_argument('--hyp', type=str, required=True, default='', 
                        help='hyp text')
    parser.add_argument('--tool', type=str, required=True, default='./sclite',
                        help='toolsclite')
    parser.add_argument('--outdir', type=str, required=True, default='', 
                        help='output dir')
    args = parser.parse_args()
    return args


def dict_ref_hyp(text):
    '''生成wavid cont词典'''
    dict_t={}
    with open(text,'r',encoding='utf-8')as fr:
        for i,line in enumerate(fr.readlines()):
            line = line.strip()
            wavid=line.split()[0]
            cont=line.split()[1:]
            # print(f'wavid为：{wavid}')
            # print(f'cont为：{cont}')
            dict_t[wavid]=' '.join(cont)
            # print(f'dict_t为：{dict_t}')
    return dict_t


def sclite_score(ref, hyp, outdir, toolsclite):
    '''转换成sclite 工具对应的ref 和 hyp 格式'''
    sclitepath=toolsclite####  slcite 路径
    reftext=ref
    hypdecode=hyp

    dict_r=dict_ref_hyp(reftext)
    dict_h=dict_ref_hyp(hypdecode)

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    refsclite=os.path.join(outdir,'ref')
    hypsclite=os.path.join(outdir,'hyp')

    with open(refsclite,'w',encoding='utf-8') as fr, open(hypsclite,'w',encoding='utf-8') as fh:
        for key in dict_r.keys() & dict_h.keys():
            fr.write('%s (%s)\n' %(dict_r[key], key))
            fh.write('%s (%s)\n' %(dict_h[key], key))
            
    cmd = '%s -h %s -r %s -c NOASCII -i wsj -e utf-8 -o all -O %s' % (sclitepath,hypsclite,refsclite,outdir)
    os.system(cmd)
    score_outfile=os.path.join(outdir,'hyp.pra') #### 输出结果文件
    if os.path.exists(score_outfile):
        return True
    else:
        return False


def read_score_file(score_outfile, ref_comparision_hyp_outfile, wer_outfile):
    """获取字错误率、句子错误率、字正确率、插入删除错误率"""
   
    f_sys = open(score_outfile,'r',encoding="utf-8")
    f_sys_content = f_sys.read()
    f_pra = open(ref_comparision_hyp_outfile,'r',encoding="utf-8")
    f_pra_content = f_pra.read()
    fout = open(wer_outfile, 'w', encoding="utf-8")

    fout.write("="*25 + ' sclite评分 ' + "="*25)
    fout.write("\n")
    # 写入 sclite 的打分结果
    fout.write(f_sys_content)
    fout.write("\n\n\n\n")
    fout.write("="*25 + ' 文本对比 ' + "="*25)
    fout.write("\n\n\n\n")
    fout.write(f_pra_content)
    fout.close()
    print("Computer WER Done")

    
def run():
    args = get_args()
    # 1. 使用sclite 计算得到 hyp.pra 文件
    res = sclite_score(args.ref, args.hyp, args.outdir, args.tool)
    # res = True
    if res:
        # score_outfile=os.path.join(args.outdir,'hyp.pra') #### 输出结果文件

        # sclite 打分的结果文件
        score_outfile=os.path.join(args.outdir,'hyp.sys')

        # sclite 输出的内容对比文件
        ref_comparision_hyp_outfile=os.path.join(args.outdir,'hyp.pra')

        # 本脚本要输出的最终文件
        wer_outfile = os.path.join(args.outdir,'result.wer')
        
        # 2. 读取 hyp.pra 生成 result.wer
        read_score_file(score_outfile, ref_comparision_hyp_outfile, wer_outfile)
        
    pass


if __name__=="__main__":
    run()
    