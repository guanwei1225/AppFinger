 # -*- coding: utf-8 -*
 #主要识别函数
import requests  #第三方模块 http://docs.python-requests.org/en/latest/
import hashlib
import re
import gzip

from lib.core.data import conf
from lib.core.data import fingerConf
from lib.core.data import fingerInfo
from lib.core.data import versionInfo
from bs4 import BeautifulSoup  

'''
import sys
reload(sys)
sys.setdefaultencoding('GBK')
'''
#更新指纹信息
def updateFingerInfo(appname,url,fingertype,finger):
	print("[%s]%s\t[%s:%s]"%(appname,url,fingertype,finger))
	if not fingerInfo.get(appname): #判断字典中是否存在对应的apps  fingerInfo:{"discuz":1}
		fingerInfo[appname] = 0   #新建字典中的app并初始化
	fingerInfo[appname] += 1   #权重加1
#更新版本信息
def updateVersionInfo(appname,url,fingertype,finger,version):
	print("[%s]%s\t[%s:%s]\t[%s]"%(appname,url,fingertype,finger,version))
	if not versionInfo.get(appname):	#判断字典中是否存在对应的apps  versionInfo:{"discuz":{"v1.0":1}}
		versionInfo[appname]={}	#新建字典中的app并初始化
		if not versionInfo[appname].get(version):	#判断字典中是否存在对应的version
			versionInfo[appname][version] = 0	#新建字典中的version并初始化
		versionInfo[appname][version] += 1	#权重加1
#对比md5值
def fingerMd5(appname):
#	print fingerConf['md5']
	for url,md5 in fingerConf['md5'].items():  #md5 = {"/index.php":"2c99e76201f38ac1a9cc9000f6ba60a5","/index1.php":"2c99e76201f38ac1a9cc9000f6ba60a5"}
		response = requests.get(conf.url+url)
		html = response.text.encode(response.encoding)  #对返回信息进行解码
		rhash = hashlib.md5(html).hexdigest()	#计算解码后的md5
		#对比md5
		if md5 == rhash:						
			updateFingerInfo(appname,conf.url+url,"md5",rhash)
#对比返回码
def fingerCode(appname):
	for url,code in fingerConf['code'].items():
		try:
			code = int(code)
		except:
			print("code must be intger")
			return
		response = requests.get(conf.url+url)
		rcode = response.status_code
		if code == rcode:
			updateFingerInfo(appname,conf.url+url,"code",str(rcode))
#对比响应头信息
def fingerHeader(appname):
	for url,header in fingerConf['header'].items():  #取header字段的值 header = {"/index.php":{"Server":"LiteSer"}}
		if type(header)!=dict:
			print("header must be a dict!")
			return
		for headerkey,headervalue in header.items(): 
			#仅支持以下头信息
			if headerkey in ['Content-Type','Content-Encoding','Content-Length','Location','Refresh','Server','Set-Cookie','WWW-Authenticate']:
				response = requests.get(conf.url+url)
				rheader = response.headers[headerkey]
				if headervalue in rheader:
					updateFingerInfo(appname,conf.url+url,"Header",rheader)
			else:
				print("Don't support header :%s"%header[0])
#对比title信息
def fingerTitle(appname):
	for url,tit in fingerConf['title'].items():
		response = requests.get(conf.url+url)
		html = response.text.encode(response.encoding)
		soup = BeautifulSoup(html,from_encoding='utf-8').title
		if soup:
#			print soup.prettify("gbk")  #在windows下要编码为gbk
			pattern = re.compile(tit,re.U)
			result = re.search(pattern,soup.string)
			if result:		#进行字符串比较
				updateFingerInfo(appname,conf.url+url,"title",result.group())
#对返回内容进行正则匹配
def fingerText(appname):
	for url,text in fingerConf['text'].items():
		response = requests.get(conf.url+url)
		html = response.text.encode(response.encoding)
		soup = BeautifulSoup(html)
#		print soup.prettify("gbk") 
#		print text
		pattern = re.compile(text)    #编译正则表达式
		result = re.search(pattern,soup.decode("utf-8"))    #以正则表达式搜索字符串
		if result:
#			print result.group()
			updateFingerInfo(appname,conf.url+url,"text",result.group())
#进行版本识别
def fingervMd5(appname):
#	print fingerConf['vmd5']
	for url,vmd5 in fingerConf['vmd5'].items():
		if type(vmd5)!=dict:
			print("vmd5's value must be a dict!")
			return
		for vmd5key,version in vmd5.items():
			response = requests.get(conf.url+url)
			html = response.text.encode(response.encoding)
			rhash = hashlib.md5(html).hexdigest()
			if vmd5key == rhash:
				updateVersionInfo(appname,conf.url + url,"md5",rhash,version)
#进行版本识别
def fingervCode(appname):
	for url,vcode in fingerConf['vcode'].items():
		if type(vCode)!=dict:
			print("vCode's value must be a dict!")
			return
		for vcodekey,version in vcode.items():
			try:
				vcodekey = int(vcodekey)
			except:
				print("code must be intger")
				return
			response = requests.get(conf.url+url)
			rcode = response.status_code
			if code == rcode:
				updateVersionInfo(appname,conf.url + url,"code",rcode,version)
#进行版本识别
def fingervTitle(appname):
	for url,vtit in fingerConf['vtitle'].items():
		if type(vtit)!=dict:
			print("title's value must be a dict!")
			return
		for tit,version in vtit.items():
			response = requests.get(conf.url+url)
			html = response.text.encode(response.encoding)
			soup = BeautifulSoup(html).title
	#		print soup.prettify("gbk")
			if tit in soup.string:
				updateVersionInfo(appname,conf.url + url,"title",tit,version)
#进行版本识别
def fingervHeader(appname):
	for url,header in fingerConf['vheader'].items():  #取header字段的值
		if type(header)!=dict:
			print("header must be a dict!")
			return
		for headerkey,headervalue in header.items():
			if type(headervalue)!=dict:
				print("header must be a dict!")
				return
			for nheader,version in headervalue.items():
				if headerkey in ['Content-Type','Content-Encoding','Content-Length','Location','Refresh','Server','Set-Cookie','WWW-Authenticate']:
					response = requests.get(conf.url+url)
					rheader = response.headers[headerkey]
					if nheader in rheader:
						updateVersionInfo(appname,conf.url + url,"header",rheader,version)
				else:
					print("Don't support header :%s"%headerkey)
#进行版本识别
def fingervText(appname):
	for url,text in fingerConf['vtext'].items():
#		print text
		if type(text)!=dict:
			print("text must be a dict!")
			return
		for textkey,version in text.items():
			response = requests.get(conf.url+url)
			html = response.text.encode(response.encoding)
			soup = BeautifulSoup(html)
	#		print soup.prettify("gbk") 
	#		print text
			pattern = re.compile(textkey)
			result = re.search(pattern,soup.decode("utf-8"))
			if result:
	#			print result.group()
				updateVersionInfo(appname,conf.url + url,"text",result.group(),version)