 # -*- coding: utf-8 -*
 #规范conf.url参数
 
import re
import urlparse
from lib.core.data import conf

def parserTargetUrl():  
	if not re.search("^http[s]*://", conf.url):
		if ":443/" in conf.url:
			conf.url = "https://" + conf.url
		else:
			conf.url = "http://" + conf.url

	__urlSplit     = urlparse.urlsplit(conf.url)
	__hostnamePort = __urlSplit[1].split(":")

	conf.scheme    = __urlSplit[0]
	conf.path      = __urlSplit[2]
	conf.hostname  = __hostnamePort[0]

	if len(__hostnamePort) == 2:
		conf.port = int(__hostnamePort[1])
		
	elif conf.scheme == "https":
		conf.port = 443
	else:
		conf.port = 80

	conf.url = "%s://%s:%d" % (conf.scheme, conf.hostname, conf.port)
	