# 简述
该项目内的代码，来自于我前段时间对中国6大云服务商提供的长语音识别API调用的测试。  
如果你需要调用同类服务，只需要配置每个以云服务商命名的文件夹下的signature文件中的内容，并按照指定的命令参数格式运行即可。  
项目中还包含了重新编译的sclite打分工具，支持超长文本的识别打分，上限是100万（1,000,000）个字符。sclite工具来自于Github项目SCTK，其软件使用协议遵从SCTK项目的协议约束。  

# 使用前的必要安装
每一家云服务商都有自己的sdk库，相应的sdk库并不包含在本项目中，需要自行安装。
- 阿里云SDK安装  
`pip install aliyunsdkcore`
- 此sdk依赖Microsoft Visual C++ 14.0或更高版本
    - 相关工具下载：https://visualstudio.microsoft.com/zh-hant/visual-cpp-build-tools/

# 语音转写(识别接口)的使用
- 阿里云  
阿里云的服务接口只支持读取文件url（其他云服务商大多也是这样，讯飞除外），因此需要预先将文件传到某个服务器的www位置，确保外网可访问。当然也可以直接使用某个云服务商的存储服务。  
每个数据集各自生成一份存储其下所有文件url的txt格式文件，每个url一行。  
以Windows为例，在powershell中运行：  
`PS > python <当前目录\csp_aliyun\long_audio_recogition.py> <url_file> <working_dir>`  
命令的参数说明：
- 参数1：存储链接的文件地址
- 参数2：你指定的工作目录

# 打分(SCTK使用说明)
- SCTK来源：
    - REPO：https://github.com/usnistgov/SCTK
    - 源码所有权归属该作者所有
    - 本项目下的工具做了重新编译，主要修改了输入文本长度限制。
        - 原版本内  
        `#define MAXSTRING 10000`
        - 本版本内  
        `#define MAXSTRING 1000000`
- SCTK的使用：
    - 系统要求：Linux / wsl
    - shell命令与参数：  
    `$ > python3 sclite_score_info_modified.py --ref <参考文本的路径> --hyp <识别文本的路径> --tool <当前路径下/SCTK/bin/sclite> --outdir <输出评分结果的目录路径>`