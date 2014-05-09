 # -*- coding: utf-8 -*
 #主函数start
from lib.core.option import *
from lib.core.progressbar import *
from lib.parse.url import parserTargetUrl
from lib.core.common import connTest
from lib.core.common import fingerApp
from lib.core.common import fingerVersion
from lib.core.common import loadPlugin
from lib.core.common import loadPlugins
from lib.core.common import showWeights
from lib.core.common import showVersion
from lib.core.common import getInformation

from lib.core.data import conf
from lib.core.data import fingerInfo
from lib.core.data import versionInfo
from lib.core.data import fingerConf

def useConf():
	if conf.url:
		#对url参数进行规范，保存至各个其他参数中
		parserTargetUrl()
		print("Target:" + conf.url)
		#首先连接目标URL，超时则返回
		status_code = connTest()
		if not status_code:
			return

		#获取目标网站信息
		if conf.information:
			getInformation()
			return
		#如果参数中配置了app，则直接识别版本
		if conf.app:
		#读取插件
			if loadPlugin(conf.app):
				fingerVersion(conf.app)
			else:
				print("no plugin for " + conf.app + " Please create it by yourself!")
		#未配置app，则加载所有插件
		plugins = loadPlugins()
		#循环加载插件
		for plugin in plugins:
			#加载插件
			if loadPlugin(plugin):
				#加载成功后识别app
				if fingerApp(plugin):
					#识别app成功后识别版本
					fingerVersion(plugin)
			#清理配置信息
			setFingerConfAttributes()

		print("\n=========END=========")
		#如果识别成功则显示结果
		if fingerInfo:
			showWeights()
			#如果识别版本成功则显示结果
			if versionInfo:
				print("=====VERSIONINFO=====")
				showVersion()
		else:
			print("cann't finger this site!")

def start():
	if conf.list:
				for url in conf.list:
					conf.url = url
					useConf()
	elif conf.url:
		useConf()


