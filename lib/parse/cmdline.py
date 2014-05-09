import sys

from optparse import OptionParser  

VERSION_STRING = "AppFinger1.0"

def cmdLineParser():
	usage = "usage: python %s [options]" %sys.argv[0]  
	parser = OptionParser(usage=usage, version=VERSION_STRING)

	parser.add_option("-u", "--url", dest="url", help="Target url")
	parser.add_option("-l", "--list", dest="list", help="Url list file")
	parser.add_option("-a", "--app", dest="app", help="AppName for example:Discuz PHPwind")
	parser.add_option("-i", "--info", dest="information", help="Get information")
	parser.add_option("-v", "--verbose", dest="verbose", help="For More details")

	(options, args) = parser.parse_args()

	return options