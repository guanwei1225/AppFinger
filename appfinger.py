 # -*- coding: utf-8 -*
 #appfinger一个判断目标网站使用app类型及版本的程序

import os
import sys
import time
import traceback

from lib.parse.cmdline import cmdLineParser
from lib.core.option import init
from lib.controller.controller import start
from lib.core.datatype import advancedDict

'''conf = advancedDict()'''
#增强程序效率
try:
	import psyco
	psyco.full()
	psyco.profile()
except ImportError, _:
	pass
#主函数
def main():
	#获取命令参数
	cmdLineOptions = cmdLineParser()
	#进行程序配置实例化、初始化
	init(cmdLineOptions)
	#开始执行程序
	start()

main()