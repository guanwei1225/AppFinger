python appfinger.py -u http://127.0.0.1 [-a app]

可自编插件，参考plugins目录下的discuz.conf.example
后缀统一使用.conf

主要指纹：
[matches]
识别方式 = json格式，数据类型为字典，非list
[version]
识别方式 = json格式，数据类型为字典，非list

格式分解：
[matches]
md5 = {"URL1":"md5值1","URL2":"md5值2"}
code = {"URL1":"状态码值1","URL2":"状态码值2"}
title = {"URL1":"title值1","URL2":"title值2"}
header = {"URL1":{"header段1":"header值1"}}
text = {"URL1":"html内容1","URL2":"html内容2"}
[version]
vmd5 = {"URL1":{"md5值1":"版本1"},"URL2":{"md5值2":"版本2"}}
其他请自行类推