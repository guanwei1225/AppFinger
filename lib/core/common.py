 # -*- coding: utf-8 -*
 #一些公共函数
from __future__ import division 

import requests  #第三方模块 http://docs.python-requests.org/en/latest/
import ConfigParser #读取配置文件
import re
import sys
import os
import simplejson as json

from progressbar import *
from finger import *
from lib.core.data import conf
from lib.core.data import fingerConf
from lib.core.data import fingerInfo
from lib.core.data import versionInfo
from bs4 import BeautifulSoup

#判断连通性
def connTest(): 
	try: 
		response = requests.get(conf.url)
		return response.status_code
	except requests.exceptions.ConnectionError:
		print("ConnectionError")
	except requests.exceptions.HTTPError:
		print("HTTPError")
	except requests.exceptions.Timeout:
		print("Timeout")
	except :
		print("Error")
#加载插件，ini+json格式
def loadPlugin(plugin):  
	#实例化config文件
	cf = ConfigParser.ConfigParser()
	#读取plugin.conf文件
	cf.read("plugins/" + plugin+".conf")
	sections = cf.sections()
	for section in sections:   
		#仅读取matches,version,info配置
		if section in ["matches","version","info"]:
			for option in  cf.options(section):  
				#仅读取支持的配置参数
				if option in ["author","version","discription","dorks","examples","md5","code","title","header","text","vmd5","vcode","vtitle","vheader","vtext"]:
					v = cf.get(section, option)
					if conf.verbose:
						print("%s:%s"%(option,v))
					try:
						#将配置内容以json格式读取					
						optioninfo = json.loads(v)
						fingerConf[option]=optioninfo
					except ValueError:
						print("wrong format of " + plugin + "!!")
						return False
	#如果配置文件信息正确，返回真
	if len(fingerConf):
		return True
	else:
		return False
#返回plugin下的.conf文件列表
def loadPlugins():
	files=[]
	for filename in os.listdir('plugins'):
		if filename[-5:] == ".conf":
			files.append(filename[:-5])
	return files
#指纹识别
def fingerApp(appname):
#	print fingerConf
	if fingerConf.md5:
		fingerMd5(appname)
	if fingerConf.code:
		fingerCode(appname)
	if fingerConf.title:
		fingerTitle(appname)
	if fingerConf.header:
		fingerHeader(appname)
	if fingerConf.text:
		fingerText(appname)		
	return fingerInfo
#版本识别
def fingerVersion(appname):
	if fingerConf.vmd5:
		fingervMd5(appname)
	if fingerConf.vcode:
		fingervCode(appname)
	if fingerConf.vtitle:
		fingervTitle(appname)
	if fingerConf.vheader:
		fingervHeader(appname)
	if fingerConf.vtext:
		fingervText(appname)
	return versionInfo
#显示指纹识别结果，权重信息
def showWeights():
	print(fingerInfo)
	total = sum(fingerInfo.values())
	sort = sorted(fingerInfo.iteritems(),key=lambda asd:asd[0],reverse = False )
#	print("sorted:")
#	print(fingerInfo)
#	print(sort)
	for keys in sort:
#		print(keys[0] + keys[1])
		print("%s => %.2f%%"%(keys[0],(keys[1]/total)*100))
#显示版本识别结果，权重信息
def showVersion():
	print(versionInfo)
	for appname,version in versionInfo.items():
		total = sum(version.values())
		sort = sorted(version.iteritems(),key=lambda asd:asd[0],reverse = False )
		for keys in sort:
	#		print(keys[0] + keys[1])
			print("[%s]%s => %.2f%%"%(appname,keys[0],(keys[1]/total)*100))

def getInformation():
	response = requests.get(conf.url)
	html = response.text.encode(response.encoding)  #对返回信息进行解码
	rhash = hashlib.md5(html).hexdigest()	#计算解码后的md5
	print("Header:")
	print(response.headers)
	print("Html:")
	soup = BeautifulSoup(html)
	print soup.prettify("gbk")
	print("Hash:")
	print(rhash)