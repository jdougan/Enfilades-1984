#
# General Enfilade as done in 1984 grant proposal.  Keys are integers,
# values are characters. This is an explicit enfilade, where values
# are stored in the bottom nodes.
#
# The node/crum format used by the grant proposal is a maximally
# expanded one, with one bottom node/crum per data element. t This is
# kind of wasteful, but it makes it easier to do bookkeeping and you
# don't have to split bottom crums/nodes.
#
# This is not idiomatic python, I'm trying to get close to the
# pseudo-code with 2 sets of changes: correctness, and changing the
# names to make more sense to a 21st century developer. If the pseudo
# code version is incorrect, it will appear with a 'Grant' suffix on
# the names.
#
# Note that a lot of the test debug output is Markdown formatted.
#
# This file uses tabs to indent

# Exception to be raised in a function to
# mark the function as unimplemented.
# Can be removed once development is over.
class NotImplemented(Exception):
	pass

# DEBUG is None means no debug output at all, Otherwise it is an
# integer with higher numbers revealing more debug data.
DEBUG = None
#
def dprint(*data, level=2):
	if (DEBUG is not None) and (DEBUG >= level):
		print(*data)

#######################################################
# keyspace/indexspace operations
#
# keys need to have operators and origin defined correctly. Model_T uses
# Integer indexes/keys. In theory you could use overloading the
# standard operators, but they might not work for the built-in types 
#
def keyZero():
	return 0
def keyAdd(posnA, widthB):
	# returns a posn in key space
	return posnA + widthB
def keySubtract(posnA, posnB):
	#returns a width/delta in key space
	return posnA - posnB
def keyEquals(a,b):
	return a == b
def keyLessThan(a,b):
	return a < b
def keyLessThanOrEqual(a,b):
	return a <= b
# not defined in the grant app, but it makes life easier for normalization
def keyMin(collKeys, lt=keyLessThan):
	assert(len(collKeys) > 0)
	if len(collKeys) == 1:
		return collKeys[0]
	mmin = collKeys[0]
	for i in range(1,len(collKeys)):
		if lt(collKeys[i], mmin):
			mmin = collKeys[i]
	return mmin

#
# Used by Enwidify/calculateWidth to keep track of 
# min/max
# This may need to be customized for each key type.
# eg. This code won't work for a 2D key.
#
class KeyBoundsSum(object):
	def __init__(self):
		self.kmin = None
		self.kmax = None
	def addDsp(self,dsp):
		if self.kmin is None:
			self.kmin = dsp
			self.kmax = dsp
		else:
			if keyLessThan(dsp, self.kmin):
				self.kmin = dsp
			if keyLessThan(self.kmax,dsp):
				self.kmax = dsp
	def width(self):
		return keySubtract(self.kmax, self.kmin)
	def minandmax(self):
		return (self.kmin, self.kmax, self.width() )


#
# 
#
def naturalWidth(d):
	return len(d)

#
# Node structure aware functions.
#
NODE_BOTTOM = 1
NODE_UPPER = 2

# For upper crums/nodes. Grant app  specs 8, I'm using 4 because it is easier to test.
# Should never be less than 3 so it doesn't degenerate into a binary tree.
MAX_CHILD_NODES = 4

class UninitializedChildren(Exception):
	pass

class Node:
    # Called a Crum in Xanaspeak.
	# TODO in future combine the data and children slots.
	# right now it is a useful backstop for debugging
	__slots__=['myNodeType', 'myDisp', 'myWidth','myData', 'myChildren']
	def __init__(node):
		node.myNodeType = None
		node.myData = None
		node.myWidth = None
		node.myDisp = None
		node.myChildren = None
	def __str__(node):
		return 'Node(' + str([node.myNodeType, node.myDisp, node.myWidth, node.myData, node.myChildren]) +  ')'
	def __repr__(node):
		return 'Node(' + str([node.myNodeType, node.myDisp, node.myWidth, node.myData, numberOfChildren(node)]) +  ')'

def createNewBottomNode():
	n = Node()
	setNodeType(n,NODE_BOTTOM)
	return n
def createNewNode():
	# aka Upper Node
	n = Node()
	setNodeType(n,NODE_UPPER)
	return n
def nodeType(node):
	return node.myNodeType
def setNodeType(node,newType):
	node.myNodeType = newType
def data(node):
	return node.myData
def setData(node, data):
	node.myData = data
def width(node):
	return node.myWidth
def setWidth(node,newWidth):
	node.myWidth = newWidth
def disp(node):
	return node.myDisp
def setDisp(node, newDisp): 
	node.myDisp = newDisp
#
#
def children(node):
	#
	# There is a potential problem when a bottom node is the single
	# and top node, the approach used to find the bottom of the
	# recursion can end up trying to find the children of a bottom
	# node (case where the single bottom node is not the data to be
	# retrieved). As a stopgap until i can discuss this with someone
	# regarding intentions I'm just going to assume a bottom node
	# returns an empty child list and log a warning for later.
	#
	# A loaf in Xanaspeak.is a collection of nodes/crums with some
	# extra bits for efficient I/O management.
	if node.myChildren is None:
		if node.myNodeType == NODE_BOTTOM:
			dprint('* BACKSTOPPED children on bottom node', level=9)
		else:
			dprint('* BACKSTOPPED children on upper node', level=9)
		return ()
	else:
		return node.myChildren
def numberOfChildren(node):
	if node.myChildren is None:
		if node.myNodeType == NODE_BOTTOM:
			dprint('* BACKSTOPPED numberOfChildren on bottom node', level=9)
		else:
			dprint('* BACKSTOPPED numberOfChildren on upper node', level=9)
		return 0
	else:
		return len(node.myChildren)

#
# Could be renamed to addChild/removeChild
# FIXME: what happens if we do  this to a bottom node?
#
def adopt(parentNode, childNode):
	if parentNode.myChildren is None :
		parentNode.myChildren = list()
	parentNode.myChildren.append(childNode)
def disown(parentNode, childNode):
	if parentNode.myChildren is None :
		raise UninitializedChildren
	parentNode.myChildren.remove(childNode)
#
# Exception raised by theOneChildOf to indicate when a collection is
# expected to have one and only one element and it does not. This
# shouldn't happen, but there are plenty of ambiguities.
# This should blow up on bottom nodes
#
class NotSingular(Exception):
	pass
def theOneChildOf(node):
	if len(node.myChildren) == 1 :
		return node.myChildren[0]
	else:
		raise NotSingular

####################################################
# Nothing below this line should be aware
# of the internal implementation structure of a Node,
#
# Impllementation of enwidify in XanaSpeak.
#
class NodesBoundsSum(KeyBoundsSum):
	def addNode(self,node):
		dprint(node)
		self.addDsp(disp(node))
		self.addDsp(keyAdd(disp(node), width(node)))
	def addChildren(self,loaf):
		for eachNode in loaf:
			self.addNode(eachNode)
def calculateWidth(*collOfCollOfNodes):
	sum = NodesBoundsSum()
	for collOfNodes in collOfCollOfNodes:
		sum.addChildren(collOfNodes)
	#dprint("!!!!!!width" , sum.width(), collOfCollOfNodes)
	return sum.width()

#
# depth counts from the bottom up, Should this blow up if there are
# malformed upper nodes with no chhildren?  FIXME
#
def depth(node):
	if node.nodeType() == NODE_BOTTOM:
		return 0
	else:
		return ( depth((children(node)[0]) )) + 1

#
# Walks the tree, using function 'of' to gather strings to show the structure.
#
def dump(node, of=print, indent=0):
	if nodeType(node) == NODE_BOTTOM :
		of("(BOTTOM", disp(node), width(node), data(node), ")")
	else:
		of("(UPPER", disp(node), width(node) )
		for each in children(node) :
			dump(each, of=of, indent=indent+1)
		of(")")

#
# Walks the tree, using of to gather strings to show the structure.
#
def dumpPretty_eoln(of=print, indent=0, lineend='\n',indentChar="\t"):
	of(lineend , end="", sep='')
	for i in range(0,indent):
		of(indentChar , end="", sep='')
def dumpPretty_print(*data, of=print):
	of(*data, end='', sep='')
def dumpPretty(node, of=dumpPretty_print, terpri=dumpPretty_eoln, indent=0):
	if nodeType(node) == NODE_BOTTOM :
		terpri(indent=indent)
		of("(BOTTOM", ' ', disp(node), ' ', width(node), ' ', repr(data(node)), ")")
	else:
		terpri(indent=indent)
		of("(UPPER", ' ', disp(node), ' ', width(node) )
		for each in children(node) :
			dumpPretty(each, of=of, indent=indent+1, terpri=terpri)
		#terpri(indent=indent)
		of(")")

#
# New helper method to make experimenting easier
#
def createOneValueEnfiladeUpperBottom(key, value):
	b = createNewBottomNode()
	setData(b, value)
	setWidth(b, naturalWidth(value))
	setDisp(b, keyZero())
	u = createNewNode()
	adopt(u,b)
	setWidth(u, calculateWidth(children(u)))
	setDisp(u, key)
	return u
def createOneValueEnfiladeBottom(key, value):
	b = createNewBottomNode()
	setData(b, value)
	setWidth(b, naturalWidth(value))
	setDisp(b, key)
	return b
def createOneValueEnfilade(key, value):
	return createOneValueEnfiladeBottom(key, value)

#
#
#
def normalizeDisps(node):
	# adjust child dsps and my disp to sum to the same but with the lowest child disp becoming keyZero
	# FIXME: add early exit on min == keyZero
	assert(numberOfChildren(node) > 0)
	childDsps  = [disp(c) for c in children(node)]
	minChildDsp = keyMin(childDsps) 
	setDisp(node, keyAdd(disp(node), minChildDsp))
	for eachChild in children(node):
		setDisp(eachChild, keySubtract( disp(eachChild) , minChildDsp ))
	return node

#
#
#
def levelPush(topNode, newNode):
	#FIXME: do  we need to do a normalizeDisps, or leave to the caller?
	newTopNode = createNewNode()
	setDisp(newTopNode, keyZero())
	setWidth(newTopNode, calculateWidth([topNode,newNode]))
	adopt(newTopNode, topNode)
	adopt(newTopNode, newNode)
	return newTopNode
#
#
#
def levelPop(topNode):
	# theOneChildOf will raise if the are 0 or >1 children
	# FIXME: do  we need to do an normalizeDisps, or leave to the caller?
	newTopNode = theOneChildOf(topNode)
	setDisp(newTopNode,  keyAdd(disp(newTopNode), disp(topNode)))
	disown(topNode, newTopNode)
	return newTopNode



#################################################################
# RETRIEVES
#

#
# Original, approx as laid out in the grant. Appears to be wrong in
# the cases where the top node has a non-zero disp, bottom node is
# the top, and when a bottom nodes data is wider than 1.
# Modified to not refer to a global topnode/fulcrum
#
def retrieveGrant(topNode, key):
	return recursiveRetrieveGrant(topNode, key, keyZero())
def recursiveRetrieveGrant(node, key, cumulativeKey):
	dprint('* ', node, 'key:' , key, 'ck:',cumulativeKey)
	# Problem: cumulatoveCey does not have top node disp adjustment
	if keyEquals(cumulativeKey, key):
		return data(node)
	else:
		for eachChild in children(node) :
			eachWidth = width(eachChild)
			eachDspStart = disp(eachChild)
			eachDspEnd = keyAdd(eachDspStart ,  eachWidth)
			# Problem: we are comparing keys in local space with keys in root space
			if keyLessThanOrEqual(eachDspStart, key) and keyLessThan(key , eachDspEnd) :
				return recursiveRetrieveGrant(eachChild, key, keyAdd(cumulativeKey, eachDspStart))

#
# Original-ish, approx as laid out in the grant. 
# Made suggested changes to return multiple results
# Appears to be wrong in the cases where retrieveGrant is wrong.
#
def retrieveAllIntoGrant(node, key, resultSet):
	recursiveRetrieveAllGrant(node, key, keyZero(), resultSet)
def recursiveRetrieveAllGrant(node, key, cumulativeKey, resultSet):
	dprint('* ', node, 'key:' , key, 'ck:',cumulativeKey)
	# Problem: cumulatoveCey does not have top node disp adjustment
	if keyEquals( cumulativeKey, key):
		resultSet.add(data(node))
	else:
		for eachChild in children(node) :
			eachWidth = width(eachChild)
			eachDspStart = disp(eachChild)
			eachDspEnd = keyAdd(eachDspStart ,  eachWidth)
			# Problem: we are comparing keys in local space with keys in root space
			if keyLessThanOrEqual(eachDspStart, key) and keyLessThan(key , eachDspEnd):
				recursiveRetrieveAllGrant(eachChild, key, keyAdd(cumulativeKey, eachDspStart), resultSet)

#
# Partially fixed.
# Only returns first solid hit.
# Probably could be cleaned up some more.
# unintuitive in cases where width of bottom node data width is > 1.
#
def retrieve(topNode, key):
	return recursiveRetrieve(topNode, key, keyAdd(keyZero(),disp(topNode)))
def recursiveRetrieve(node, keyInRootSpace, cumulativeKey):
	dprint('* Node start:' , node, 'keyInRoot:' , keyInRootSpace, 'ckInRoot:', cumulativeKey)
	if (nodeType(node) == NODE_BOTTOM):
		if keyEquals( cumulativeKey, keyInRootSpace ):
			return data(node)
	else:
		# translate the key into local key space
		keyInLocalSpace = keySubtract(keyInRootSpace, cumulativeKey)
		for eachChild in children(node) :
			eachDspStart = disp(eachChild)
			eachWidth = width(eachChild)
			eachDspEnd = keyAdd(eachDspStart ,  eachWidth)
			dprint('    * Child startDsp:', eachDspStart, 'wid:', eachWidth, 'localKey:', keyInLocalSpace, 'endDsp:', eachDspEnd)
			if keyLessThanOrEqual(eachDspStart, keyInLocalSpace) and keyLessThan(keyInLocalSpace , eachDspEnd) :
				return recursiveRetrieve(eachChild, keyInRootSpace, keyAdd(cumulativeKey, eachDspStart))

#
# Original-ish, approx as laid out in the grant. 
# Made alternate changes to return multiple results
# using a gathering function
#
def retrieveAllInto(node, keyInRootSpace, resultSet):
	def gatherFn(datum, dataNode=None):
		resultSet.add(datum)
	retrieveAllFn(node, keyInRootSpace, gatherFn)
	return resultSet
def retrieveAllIntoList(node, keyInRootSpace, resultList):
	def gatherFn(datum, dataNode=None):
		resultList.append(datum)
	retrieveAllFn(node, keyInRootSpace, gatherFn)
	return resultList
#
def retrieveAllFn(node, keyInRootSpace, fn):
	recursiveRetrieveAllFn(node, keyInRootSpace, keyAdd(keyZero(),disp(node)), fn)
def recursiveRetrieveAllFn(node, keyInRootSpace, cumulativeKey, fn):
	dprint('* Node start:' , node, 'keyInRoot:' , keyInRootSpace, 'ckInRoot:', cumulativeKey)
	if ( nodeType(node) == NODE_BOTTOM  ):
		if keyEquals( cumulativeKey, keyInRootSpace ):
			fn(data(node), node)
		else:
			pass
	else:
		# translate  the key into local key space
		keyInLocalSpace = keySubtract(keyInRootSpace, cumulativeKey)
		for eachChild in children(node) :
			eachDspStart = disp(eachChild)
			eachWidth = width(eachChild)
			eachDspEnd = keyAdd(eachDspStart ,  eachWidth)
			dprint('    * Child startDsp:', eachDspStart, 'wid:', eachWidth, 'localKey:', keyInLocalSpace, 'endDsp:', eachDspEnd)
			if keyLessThanOrEqual(eachDspStart, keyInLocalSpace) and keyLessThan(keyInLocalSpace , eachDspEnd) :
				recursiveRetrieveAllFn(eachChild, keyInRootSpace, keyAdd(cumulativeKey, eachDspStart), fn)

#
# Experiment using nested fns
#
def retrieveAllIntoList2(rootNode, keyInRootSpace, resultList):
	def gatherFn(datum, dataNode=None):
		resultList.append(datum)
	retrieveAll2(rootNode, keyInRootSpace, gatherFn)
	return resultList
def retrieveAll2(rootNode, keyInRootSpace, fn):
	def recursiveRetrieveAll(node, cumulativeKey):
		dprint('* Node start:' , node, 'keyInRoot:' , keyInRootSpace, 'ckInRoot:', cumulativeKey)
		if keyEquals( cumulativeKey, keyInRootSpace ):
			fn(data(node), node)
		else:
			# translate  the key into local key space
			keyInLocalSpace = keySubtract(keyInRootSpace, cumulativeKey)
			for eachChild in children(node) :
				eachDspStart = disp(eachChild)
				eachWidth = width(eachChild)
				eachDspEnd = keyAdd(eachDspStart ,  eachWidth)
				dprint('    * Child startDsp:', eachDspStart, 'wid:', eachWidth, 'localKey:', keyInLocalSpace, 'endDsp:', eachDspEnd)
				if keyLessThanOrEqual(eachDspStart, keyInLocalSpace) and keyLessThan(keyInLocalSpace , eachDspEnd) :
					recursiveRetrieveAll(eachChild, keyAdd(cumulativeKey, eachDspStart))
	#
	recursiveRetrieveAll(node, keyInRootSpace, keyAdd(keyZero(),disp(node)), fn)

##################################################
# APPENDS
#
# The intended usage of the where and beyond parameters in unclear in
# the docs

#
#
#
def appendGrant(topNode, whereKey, beyond, newDomainValue):
	# returns a new topnode
	# original referred to a global top node/fulcrum, but we don't
	# want globals if we can help it
	#
	potentialNewNode = recursiveAppend(topNode, whereKey, beyond, newDomainValue)
	if potentialNewNode is not None:
		return levelPush(topNode, potentialNewNode)
	else:
		return topNode
#
def recursiveAppendGrant(parentNode, whereKey, beyond, newDomainThing):
	if keyEquals(whereKey, keyZero()):
		newNode = createNewBottomNode()
		setData(newNode, newDomainThing)
		setWidth(newNode, naturalWidth(newDomainThing))
		setDisp(newNode, keyAdd(disp(parentNode), beyond))
		return newNode
	else:
		potentialNewNode = None
		for eachChild in children(parentNode):
			if keyLessThanOrEqual(disp(eachChild), whereKey) and keyLessThan(whereKey, keyAdd(disp(eachChild), width(eachChild))):
				potentialNewNode = recursiveAppend(eachChild, keySubtract(whereKey, disp(eachChild)), beyond, newDomainThing)
				break
		if potentialNewNode is not None:
			if numberOfChildren(parentNode) >= MAX_CHILD_NODES:
				newNode = createNewNode()
				setDisp(newNode, disp(potentialNewNode))
				setDisp(potentialNewNode, keyZero())
				setWidth(newNode, width(potentialNewNode))
				# PROBLEM, isn't adopting
				return newNode
			else:
				setWidth(parentNode, calculateWidth(children(parentNode), [potentialNewNode]))
				adopt(parentNode, potentialNewNode)
				return None
		else:
			return None

#
#
#
def append(topNode, topWhereKey, beyond, newDomainValue):
	# FIXME: I'm not happy with the scattershot use of normalizeDisps,
	# need to look at more targeted use.
	# There are a lot of debug prints here, reorg them.
	if topNode is None:
		return createOneValueEnfilade(keyAdd(topWhereKey, beyond), newDomainValue)
	# may return a new topnode
	potentialNewNode = recursiveAppend(topNode, keySubtract(topWhereKey, disp(topNode)), beyond, newDomainValue)
	dprint("* Potential New Node" , potentialNewNode )
	if potentialNewNode is not None:
		return normalizeDisps(levelPush(topNode, potentialNewNode))
	else:
		return normalizeDisps(topNode)
#
def recursiveAppend(parentNode, whereKey, beyond, newDomainThing):
	if DEBUG is not None:
		myArgs = [parentNode, whereKey]
	else:
		myArgs = None
	dprint("* StartRA1", myArgs)
	if (nodeType(parentNode) == NODE_BOTTOM) :
		if keyEquals(whereKey, keyZero()):
			dprint("    * bottom node creation", myArgs)
			newNode = createNewBottomNode()
			setData(newNode, newDomainThing)
			setWidth(newNode, naturalWidth(newDomainThing))
			setDisp(newNode, keyAdd(disp(parentNode), beyond))
			dprint("* EndRA1", myArgs, newNode)
			return newNode
		else:
			raise KeyError("At Bottom node, key not matching: " + str(parentNode))
	else:
		potentialNewNode = None
		dprint("    * search", children(parentNode))
		for eachChild in children(parentNode):
			if keyLessThanOrEqual(disp(eachChild), whereKey) and keyLessThan(whereKey, keyAdd(disp(eachChild), width(eachChild))):
				potentialNewNode = recursiveAppend(eachChild, keySubtract(whereKey, disp(eachChild)), beyond, newDomainThing)
				break
		dprint("        * hit?", potentialNewNode)
		if potentialNewNode is not None:
			if numberOfChildren(parentNode) >= MAX_CHILD_NODES:
				dprint("    * upper node creation", myArgs)
				newNode = createNewNode()
				setDisp(newNode, keyAdd(disp(potentialNewNode),disp(parentNode)))
				setDisp(potentialNewNode, keyZero())
				setWidth(newNode, width(potentialNewNode))
				adopt(newNode, potentialNewNode)
				normalizeDisps(parentNode)
				dprint("* EndRA1", myArgs , newNode)
				return newNode
			else:
				dprint("    * upper node adoption", myArgs)
				setWidth(parentNode, calculateWidth(children(parentNode), [potentialNewNode]))
				adopt(parentNode, potentialNewNode)
				normalizeDisps(parentNode)
				dprint("* EndRA1", myArgs, beyond, newDomainThing)
				return None
		else:
			setWidth(parentNode, calculateWidth(children(parentNode)))
			normalizeDisps(parentNode)
			dprint("* EndRA1 no match", myArgs)
			return None

#
#
#
def append1(topNode, topWhereKey, beyond, newDomainThing):
	# reorg append to use nested functions to make experiments no mess
	# with other parts of the file
	# FIXME: I'm not happy with the scattershot use of normalizeDisps,
	# need to look at more targeted use.
	# There are a lot of debug prints here, reorg them.
	def recursiveAppend(parentNode, whereKey):
		if DEBUG is not None:
			myArgs = [parentNode, whereKey]
		else:
			myArgs = None
		dprint("* StartRA1", myArgs)
		if (nodeType(parentNode) == NODE_BOTTOM) :
			if keyEquals(whereKey, keyZero()):
				dprint("    * bottom node creation", myArgs)
				newNode = createNewBottomNode()
				setData(newNode, newDomainThing)
				setWidth(newNode, naturalWidth(newDomainThing))
				setDisp(newNode, keyAdd(disp(parentNode), beyond))
				dprint("* EndRA1", myArgs, newNode)
				return newNode
			else:
				raise KeyError("At Bottom node," + str(topWhereKey) + " key not matchingin node " + str(parentNode))
		else:
			potentialNewNode = None
			dprint("    * search", children(parentNode))
			for eachChild in children(parentNode):
				if keyLessThanOrEqual(disp(eachChild), whereKey) and keyLessThan(whereKey, keyAdd(disp(eachChild), width(eachChild))):
					potentialNewNode = recursiveAppend(eachChild, keySubtract(whereKey, disp(eachChild)))
					break
			dprint("        * hit?", potentialNewNode)
			if potentialNewNode is not None:
				if numberOfChildren(parentNode) >= MAX_CHILD_NODES:
					dprint("    * upper node creation", myArgs)
					newNode = createNewNode()
					setDisp(newNode, keyAdd(disp(potentialNewNode),disp(parentNode)))
					setDisp(potentialNewNode, keyZero())
					setWidth(newNode, width(potentialNewNode))
					adopt(newNode, potentialNewNode)
					normalizeDisps(parentNode)
					dprint("* EndRA1", myArgs , newNode)
					return newNode
				else:
					dprint("    * upper node adoption", myArgs)
					setWidth(parentNode, calculateWidth(children(parentNode), [potentialNewNode]))
					adopt(parentNode, potentialNewNode)
					normalizeDisps(parentNode)
					dprint("* EndRA1", myArgs, beyond, newDomainThing)
					return None
			else:
				setWidth(parentNode, calculateWidth(children(parentNode)))
				normalizeDisps(parentNode)
				dprint("* EndRA1 no match", myArgs)
				return None
	#
	#
	#
	if topNode is None:
		return createOneValueEnfilade(keyAdd(topWhereKey, beyond), newDomainThing)
	# may return a new topnode
	potentialNewNode = recursiveAppend(topNode, keySubtract(topWhereKey, disp(topNode)))
	dprint("* Potential New Node" , potentialNewNode )
	if potentialNewNode is not None:
		return normalizeDisps(levelPush(topNode, potentialNewNode))
	else:
		return normalizeDisps(topNode)


###################################################################
# Tree cutting
# Helper functions are my guess at intent.
#
# is child set a set? I think it is just a pair
#
def makeChildSet(left, right):
	return [left, right]
def leftChild(childSet):
	return childSet[0]
def rightChild(childSet):
	return childSet[-1]
#
# is cut set a set? I think it is a sorted collection of root space
# disps. FIXME: How many cuts in a set? Can't be 0, maybe minimum of one?
# test.
#
def makeCutSet(*cuts, sortFn=keyLessThan):
	# cuts is a yuple of cut keys
	return sorted(cuts, key=sortFn)
def makeCutSetAll(*cutsList, sortFn=keyLessThan):
	# cutsList is a tuple of lists of cut keys
	return sorted(cuts, key=sortFn)
def firstCut(cutSet):
	return cutSet[0]
def lastCut(cutSet):
	return cutSet[-1]
#
#
#
def cutGrant(cutSet, topNode):
	recursiveCutGrant(cutSet, topNode)
	return topNode
#
def recursiveCutGrant(cutSet, parentNode):
	dontDiveDeeperFlag = True
	for eachChild in children(parentNode):
		if keyLessThan(disp(eachChild), firstCut(cutSet)) and keyLessThanOrEqual(lastCut(cutSet), keyAdd(disp(eachChild), width(eachChild))) :
			dontDiveDeeperFlag = False
			for eachCut in cutSet:
				# FIXME: Is this supposed to change the cutSet entry in place?
				raise NotImplemented
				eachCut = keySubtract(eachCut, disp(eachChild) )
			recursiveCutGrant(cutSet, eachChild)
	if dontDiveDeeperFlag:
		chopUpGrant(cutSet, parentNode)
#
def chopUpGrant(cutSet, parentNode):
	for eachCut in cutSet:
		for eachChild in children(parentNode):
			if keyLessThan(disp(eachChild), cut) and keyLessThanOrEqual(cut, keyAdd(disp(eachChild), width(eachChild))):
				newChildSet = splitGrant(cut, eachChild)
				disown(parentNode, child)
				adopt(parentNode, leftChild(newChildSet))
				adopt(parentNode, rightChild(newChildSet))
				break
#
def splitGrant(cut, node):
	leftNode = createNewNode()
	rightNode = createNewNode()
	setDisp(leftNode, disp(node))
	setWidth(leftNode, keySubtract(cut, disp(node)))
	setDisp(rightNode, cut)
	setWidth(rightNode, keySubtract(keyAdd(width(node), disp(node)), cut) )
	for eachChild in children(node):
		if keyLessThan(keyAdd(disp(eachChild), width(eachChild)), cut) :
			adopt(leftNode, eachChild)
		elif keyLessThanOrEqual(cut, disp(eachChild)) :
			adopt(rightNode, eachChild)
		else:
			newChildSet = splitGrant(keySubtract(cut, disp(eachChild)), eachChild)
			adopt(leftNode, leftChild(newChildSet))
			adopt(rightNode, rightChild(newChildSet))
	#
	return makeChildSet(leftNode, rightNode)

#######################################################
# You may not want to recombination is you're tree node sharing.
#
#
#
def prmitiveRecombineGrant(parentNode, sibling1, sibling2):
	newNode = createNewNode()
	setDisp(newNode, disp(sibling1))
	for eachChild in children(sibling1):
		disown(sibling1, eachChild)
		adopt(newNode, eachChild)
	dispCorrection = keySubtract(disp(sibling2), disp(siblng1))
	for eachChild in children(sibling2):
		disown(sibling2, eachChild)
		setDisp(eachChild, keyAdd(disp(eachChild), dispCorrection))
		adopt(newNode, eachChild)
	setWidth(newNode, calculateWidth(children(newNode)))
	disown(parentNode, sibling1)
	disown(parentNode, sibling2)
	adopt(parentNode, newNode)



