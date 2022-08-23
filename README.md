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