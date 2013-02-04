#!/usr/bin/env python

import sys,getopt
import parse

def usage():
    print """
    
    	python %s -a <arcsfile> -v <verticesfile>

    Options are:
    	-h	Desplay the usage menu.
	-a	Arcs file name.
	-v	Vertices file name
    """ % (sys.argv[0])

def main():
    if len(sys.argv) < 3:
    	usage()
	sys.exit(0)
    else:
    	try:
		opts, args = getopt.getopt(sys.argv[1:], "ha:v:", ["help", "arcs=", "vertics="])
    	except getopt.GetoptError, err:
		print str(err)
		#usage()
		sys.exit(1)
    arcsfile = ''
    verticsfile = ''

    for o, a in opts:
    	if o in ("-h", "--help"):
		usage()
		sys.exit(0)
	elif o in ("-a", "--arcs"):
		arcsfile = a
	elif o in ("-v", "--vertics"):
		verticsfile = a
    
    if arcsfile == '' or verticsfile == '':
    	print "You must specify both vertics file and arcs file to begin."
	sys.exit(0)
    
    arcs = open(arcsfile, 'r')
    vertics = open(verticsfile, 'r')
    #print arcs.readlines()
    parse.parse(arcs,vertics)

if __name__ == '__main__':
    main()
