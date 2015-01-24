import LRParser
import sys
print 'MUA programming language'
print 'Version 1.0'
print 'Build By DarkTango'
if len(sys.argv) != 2:
	print 'usage: python mua.py [filename]'
	exit(0)

print '**************************************************'
fileobj = open(sys.argv[1])
LRParser.run(fileobj.read())
fileobj.close()
