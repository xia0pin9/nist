"""
Parser to process the attack graph data, and extract the nodes and edges, construct the final attack graph check table.
"""

import string, re, sys

vtemptable = {}
atemptable = {}
table = {}
stack = []


# Extract the nodes and edges set for later use
def parse(arcs, vertics):
    global vtemptable
    global atemptable
    global table
    startpoint = 0
    target = ''
    arcslines = arcs.readlines()
    verticslines = vertics.readlines()
    
    #extract host entities on the attack graph
    for vline in verticslines:
    	vtemp = vline.split(",\"")
	m1 = string.rstrip(vtemp[1], "\"")
	m2 = vtemp[2].split("\",")[0]
	vtemptable[vtemp[0]] = (m1, m2, -1)
	if m1.startswith("attackerLocated"):
	    startpoint = vtemp[0]
	    m = re.search('(?<=\()\w+', m1)
	    table[m.group()] = []
	if m1.startswith("execCode"):
	    m = re.search('(?<=\()\w+', m1)
	    if int(vtemp[0]) != 1:
	    	table[m.group()] = []
  	    else:
	    	target = m.group()
		continue
	if m1.startswith("accessFile"):
	    m = re.search('(?<=\()\w+', m1)
	    table[m.group()] = []
    for aline in arcslines:
    	atemp = aline.split(",")
	if not vtemptable[atemp[1]][0].startswith("attackerLocated") and vtemptable[atemp[1]][1] == "LEAF" and not "vulExists" in vtemptable[atemp[1]][0]:
	    continue
	elif vtemptable[atemp[1]][1] == "LEAF" and "vulExists" in vtemptable[atemp[1]][0]:
	    vtemptable[atemp[0]]= (vtemptable[atemp[1]][0], vtemptable[atemp[0]][1], -1)
	elif atemp[1] not in atemptable:
	    atemptable[atemp[1]] = [atemp[0]]
	else:
	    atemptable[atemp[1]].append(atemp[0])
    if target in table:
    	del table[target]
    dfs(startpoint)
    print table
    #for node in table:
    #	print table[node]


# depth first search algorithm to traverse the attack graph from starting node
def dfs(start):
    global table
    global stack
    nodetuple = (vtemptable[start][0], vtemptable[start][1],0)
    vtemptable[start] = nodetuple
    host = re.search('(?<=\()\w+', vtemptable[start][0])
    stack.append(host.group())
    for nextnode in findNext(start) :
    	if vtemptable[nextnode[1]][0].startswith("execCode") or "(NFS shell)" in vtemptable[nextnode[0]][0]:
            target = re.search('(?<=\()\w+', vtemptable[nextnode[1]][0])
	    if host.group() == target.group():
	    	temphost = stack.pop()
	    	while temphost == target.group():
			temphost = stack.pop()
	    else:
	    	temphost = host.group()
	    if temphost in table:
		table[temphost].append((vtemptable[nextnode[0]][0],target.group()))
	    stack.append(temphost)
	if vtemptable[nextnode[1]][2] == -1:
	    	dfs(nextnode[1])
	#elif vtemptable[nextnode[1]][2] == 1:
	#    continue
    nodetuple = (nodetuple[0], nodetuple[1], 1)
    vtemptable[start] = nodetuple

def findNext(node):
    output = []
    if node in atemptable:
	for nextnode in atemptable[node]:
	    output.append((nextnode, atemptable[nextnode][0]))
    return output
    #print startpoint
	    #table[temptable[atemp[1][1]] = [temptable[atemp[0]][1],]
	    #else:
	    #    #table[temptable[atemp[1][1]].append(temptable[atemp[0]][1])
