def parse(arcs, vertics):
    temptable = {}
    table = {}
    arcslines = arcs.readlines()
    verticslines = vertics.readlines()
    for vline in verticslines:
    	vtemp = vline.split(",")
	temptable[vtemp[0]] = (vtemp[1],vtemp[2])
    for aline in arcslines:
    	atemp = aline.split(",")
	if (atemp[1] not in table) and atemp[0] != 1:
    	    print temptable
    #print table    
    
