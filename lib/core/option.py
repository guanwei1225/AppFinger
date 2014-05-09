# -*- coding: utf-8 -*
#做一些初始化的动作，判断输入参数的合法性

from lib.core.data import conf
from lib.core.datatype import advancedDict
from lib.core.data import fingerConf
from lib.core.data import fingerInfo


def __setConfAttributes():
	conf.url	=	""
	conf.list   =	[]
	conf.app	=	""
	conf.version =	""
	conf.scheme	=	""
	conf.path	=	""
	conf.hostname =	""
	conf.port	=	80


def setFingerConfAttributes():
	fingerConf.author	=	""
	fingerConf.version	=	""
	fingerConf.discription=	""
	fingerConf.dorks	=	""
	fingerConf.examples =	""

	fingerConf.md5		=	{}
	fingerConf.code		=	{}
	fingerConf.title	=	{}
	fingerConf.header	=	{}
	fingerConf.text 	=	{}

	fingerConf.vmd5		=	{}
	fingerConf.vcode	=	{}
	fingerConf.vtitle	=	{}
	fingerConf.vheader	=	{}
	fingerConf.vtext 	=	{}


def init(inputOptions = advancedDict()):

	__setConfAttributes() #初始化参数
	setFingerConfAttributes() #初始化FingerConf

	if inputOptions.list: #如果有-l参数，则读取文件，保存在list中
		f = open(inputOptions.list)
		for line in f.readlines():
			print line.strip()
			conf.list.append(line.strip())
		print(conf.list)

	elif not inputOptions.url: #必须存在-l或-u参数之一以确定目标地址
		print("You must give one of '-l' or '-u' option")
		return False

	conf.url = inputOptions.url
	conf.app = inputOptions.app
	conf.information =	inputOptions.information
	conf.verbose =	inputOptions.verbose