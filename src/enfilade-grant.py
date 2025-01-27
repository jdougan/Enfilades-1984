#
# General Enfilade as done in 1984 grant proposal.  Keys are integers,
# values are characters strings. This is an explicit enfilade, where values
# are stored in the bottom nodes. This is NOT a Model-T,
# in a Model-T the disps are implicit in the sequencing.
#
# The node/crum format used by the grant proposal is a maximally
# expanded one, with one bottom node/crum per data element. This is
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

import functools

# Exception to be raised in a function to
# mark the function as unimplemented.
# Can be removed once development is over.
class NotImplemented(Exception):
	pass

# DEBUG is None means no debug output at all, Otherwise it is an
# integer with higher numbers revealing more debug data.
DEBUG = None
DEFAULT_DPRINT_LEVEL = 2
#
def dprint_normal(*data, level=DEFAULT_DPRINT_LEVEL, of=print):
	if (DEBUG is not None) and (DEBUG >= level):
		of(*data)
def dprint_off(*data, **datak):
	pass
dprint = dprint_normal

def countSlot(val):
	if val is None:
		return val
	else:
		return len(val)

IPRINT_INDENT_LEVEL=0
IPRINT_INDENT_SEGMENT='    '

def iprintResetLevel(level=0):
	global IPRINT_INDENT_LEVEL
	IPRINT_INDENT_LEVEL=level
def iprint(*data, level=0, of=print):
	global IPRINT_INDENT_LEVEL
	global IPRINT_INDENT_SEGMENT
	for i in range(IPRINT_INDENT_LEVEL):
		of(IPRINT_INDENT_SEGMENT, end='')
	of(*data)
	IPRINT_INDENT_LEVEL = IPRINT_INDENT_LEVEL + level


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

#
# FIXME added to make python sorted() work
# probably needs to be rethought as they changed
# how sorts are specified in python3
#
def keyCmp(a,b):
    return bool(a > b) - bool(a < b)

# not defined in the grant app, but it makes life easier for
# normalization
# This may need to be customized for each key type.
# eg. This code won't work for a 2D key.
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

KeyType = int
ValueType = str

#
# Assumes d is a string
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

class InvalidChildren(Exception):
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
		return 'Node(' + str([node.myNodeType, node.myDisp, node.myWidth, node.myData, node.myChildren]) +  ')'
	def shortDesc(node):
		return 'Node(' + str([node.myNodeType, node.myDisp, node.myWidth, node.myData, countSlot(node.myChildren)]) +  ')'

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
	# There was a problem when a bottom node is the single
	# and top node, the approach used to find the bottom of the
	# recursion can end up trying to find the children of a bottom
	# node (case where the single bottom node is not the data to be
	# retrieved). Backstop no longer necessary as I now understand
	# the issues, now throw an exception to indicate something has gone horribly wrong.
	#
	# A loaf in Xanaspeak.is a collection of nodes/crums with some
	# extra bits for efficient I/O management.
	if node.myChildren is None:
		if node.myNodeType == NODE_BOTTOM:
			raise InvalidChildren("Bottom Node in children()")
		return ()
	else:
		return node.myChildren
def numberOfChildren(node):
	if node.myChildren is None:
		if node.myNodeType == NODE_BOTTOM:
			raise InvalidChildren("Bottom Node in numberOfChildren()")
		return 0
	else:
		return len(node.myChildren)

#
# Could be renamed to addChild/removeChild
# FIXME: what happens if we do this to a bottom node?
#
def adopt(parentNode, childNode):
	if parentNode.myNodeType == NODE_BOTTOM:
		raise InvalidChildren("Bottom Node in adopt()")
	if parentNode.myChildren is None :
		parentNode.myChildren = list()
	assert(numberOfChildren(parentNode) < MAX_CHILD_NODES )
	parentNode.myChildren.append(childNode)
def disown(parentNode, childNode):
	if parentNode.myNodeType == NODE_BOTTOM:
		raise InvalidChildren("Bottom Node in disown()")
	if parentNode.myChildren is None :
		raise InvalidChildren("Uppper Node in disown()")
	assert(childNode in parentNode.myChildren)
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
	if node.myNodeType == NODE_BOTTOM:
		raise InvalidChildren("Bottom Node in theOneChildOf()")
	#if parentNode.myChildren is None :
	#	raise InvalidChildren("Uppper Node in theOneChildOf()")
	if len(node.myChildren) == 1 :
		return node.myChildren[0]
	else:
		raise NotSingular("theOneChildOf()")

####################################################
# Nothing below this line should be aware
# of the internal implementation structure of a Node,
#
# Implementation of Enwidify in XanaSpeak.
#
class NodesBoundsSum(KeyBoundsSum):
	def addNode(self,node):
		dprint(node)
		self.addDsp(disp(node))
		self.addDsp(keyAdd(disp(node), width(node)))
	def addChildren(self,collOfNodes):
		for eachNode in collOfNodes:
			self.addNode(eachNode)
def calculateWidth(*collOfCollOfNodes):
	sum = NodesBoundsSum()
	for collOfNodes in collOfCollOfNodes:
		sum.addChildren(collOfNodes)
	#dprint("!!!!!!width" , sum.width(), collOfCollOfNodes)
	return sum.width()

#
# depth counts from the bottom up, Should this blow up if there are
# malformed upper nodes with no children?  FIXME
# count from one so an empty tree is zero depth
#
def depth(node):
	if node is None:
		return 0
	if nodeType(node) == NODE_BOTTOM:
		return 1
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
def dumpPretty(node, of=dumpPretty_print, terpri=dumpPretty_eoln, indent=0, childSort=False):
	if nodeType(node) == NODE_BOTTOM :
		terpri(indent=indent)
		of("(BOTTOM", ' ', disp(node), ' ', width(node), ' ', repr(data(node)), ")")
	else:
		terpri(indent=indent)
		of("(UPPER", ' ', disp(node), ' ', width(node) )
		if childSort :
			for each in sorted(children(node), key=disp) :
				dumpPretty(each, of=of, indent=indent+1, terpri=terpri)
		else:
			for each in children(node):
				dumpPretty(each, of=of, indent=indent+1, terpri=terpri)			
		#terpri(indent=indent)
		of(")")


def breadthTraverseNodes(node, fn):
	fn(node)
	if nodeType(node) == NODE_UPPER	:
		for eachChild in children(node):
			breadthTraverseNodes(eachChild, fn)

def depthTraverseNodes(node, fn):
	if nodeType(node) == NODE_UPPER	:
		for eachChild in children(node):
			depthTraverseNodes(eachChild, fn)
	fn(node)

def validateNode(node,errs=list()):
	# FIXME: needss generalizing for complex Key types
	if type(width(node)) is not KeyType:
		errs.append( ('Wrong Key Type width', node) )
	if type(disp(node)) is not KeyType:
		errs.append( ('Wrong Key Type disp', node) )
	if nodeType(node) == NODE_BOTTOM:
		if type(data(node)) is not ValueType:
			errs.append( ('Wrong Value Type data', node) )
		if naturalWidth(data(node)) != width(node):
			errs.append( ('Width Mismatch Bottom', node) )
	else:
		if len(children(node)) > MAX_CHILD_NODES:
			errs.append( ('Invalid Children too many', node) )
		if len(children(node)) < 1:
			errs.append( ('Invalid Children empty', node) )
	return errs

def validateNodes(top, errs=list()):
	validateNode(node, errs)
	if nodeType(node) == NODE_UPPER:
		for eachChild in children(node):
			validateNodes(eachChild, errs)
	return errs



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
#
#
def traverseValuesIntoList(node, out=list()):
	# unordered
	def tupleAppend(data, key, node):
		out.append(data)
	traverseValuesFn(node, tupleAppend)
	return out
def traverseValuesFn(node, fn3):
	# unordered
	def recursiveTraverseValuesFn(node, cumulativeKey, fn3):
		if ( nodeType(node) == NODE_BOTTOM  ):
			fn3(data(node), cumulativeKey , node=node)
		else:
			for eachChild in children(node) :
				eachDspStart = disp(eachChild)
				recursiveTraverseValuesFn(eachChild, keyAdd(cumulativeKey, eachDspStart), fn3)
	recursiveTraverseValuesFn(node, keyAdd(keyZero(),disp(node)), fn3)


#
# Experiment using nested fns
# and more intuitive retrieval
#
def retrieveAllIntoList2(rootNode, keyInRootSpace, resultList=list()):
	def gatherFn(*args):
		resultList.append(args)
	retrieveAll2(rootNode, keyInRootSpace, gatherFn)
	return resultList

def retrieveAll2(rootNode, keyInRootSpace, fn):
	def recursiveRetrieveAll(node, cumulativeKey):
		dprint('* Node start:' , node, 'keyInRoot:' , keyInRootSpace, 'ckInRoot:', cumulativeKey)
		if nodeType(node) == NODE_BOTTOM :
			# if we get here, what we want in in the data, but
			# isn't necessarily in the first position.
			offset = keySubtract(keyInRootSpace, cumulativeKey)
			fn(data(node)[offset], offset, cumulativeKey, keyInRootSpace)
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
	recursiveRetrieveAll(rootNode, keyAdd(keyZero(),disp(rootNode)))

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
	# FIXME breaks sometimes on overlapping data with naturalWid > 1
	# This appears to be because it is finding a subnode  where the target key
	# is not the first element of the hit, so the test fails. Not sure
	# of the correct solutions 
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
			raise KeyError(f"Bottom node {parentNode}, key {whereKey} not matching {keyZero()}." )
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
	# FIXME breaks sometimes on overlapping data with naturalWid > 1
	# This appears to be because it is finding a subnode  where the target key
	# is not the first element of the hit, so the test fails. Not sure
	# of the correct solutions 
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
# is child set a set? I think it is just a pair. Could be replaced in
# python with a tuple multi-value return.
#
def makeChildSet(left, right):
	return [left, right]
def leftChild(childSet):
	return childSet[0]
def rightChild(childSet):
	return childSet[-1]
#
# is cut set a set? I think it is a sorted collection of root space
# disps. FIXME: Minimum cuts in a set? Can't be 0, maybe minimum of one?
# TODO test.
# see https://docs.python.org/3/howto/sorting.html for the sorted use
#
def makeCutSet(*cuts, sortFn=keyCmp):
	# cuts is a yuple of cut keys
	return sorted(cuts, key=functools.cmp_to_key(sortFn))
def makeCutSetAll(cutsList, sortFn=keyCmp):
	# cutsList is a tuple of lists of cut keys
	return sorted(cutsList, key=functools.cmp_to_key(sortFn))
def firstCut(cutSet):
	return cutSet[0]
def lastCut(cutSet):
	return cutSet[-1]
def cloneCutSet(cutSet):
	return cutSet.copy()
#
# Hideously broken, AFAICT
#
def cutGrant(cutSet, topNode):
	recursiveCutGrant(cutSet, topNode)
	return topNode
#
def recursiveCutGrant(cutSet, parentNode):
	dontDiveDeeperFlag = True
	for eachChild in children(parentNode):
		# tests need checking
		if keyLessThan(disp(eachChild), firstCut(cutSet)) and keyLessThanOrEqual(lastCut(cutSet), keyAdd(disp(eachChild), width(eachChild))) :
			dontDiveDeeperFlag = False
			# WARNING broken magic
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
				# same node overfilling problem here as in split
				newChildSet = splitGrant(cut, eachChild)
				disown(parentNode, child)
				adopt(parentNode, leftChild(newChildSet))
				adopt(parentNode, rightChild(newChildSet))
				break
#
# split is where most of the magic is supposed to happen in cut.
#
# After hacking around it it looks pretty wrong. will the new node
# width calculations work with data with holes in it? No
# normalization step, disps will be wrong. With naturalWid == 1 data,
# we should never be trying to split bottom nodes. If we need to,
# write a separate case based om the specific needs of the data
# Besides, the rest of the grant code doesn't handle that case very
# well. Another issue is overfilling the parent node with children
# when you generate two new nodes after a split but only remove one.
#
def splitGrant(cut, node):
	leftNode = createNewNode()
	rightNode = createNewNode()
	# unclear if these widths ans disps are correct or need re-normalization
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

#
#
#
def cut(cutSet, topNode):
	iprint()
	iprint("- cut(" , cutSet , ",  ", topNode.shortDesc(), ')', level=1)
	recursiveCut(cutSet, topNode)
	iprint('- return cut', level=-1)
	return topNode
#
def recursiveCut(cutSet, parentNode):
	iprint("- recursiveCut(", cutSet, '    ' , parentNode.shortDesc(), ')', level=1)
	dontDiveDeeperFlag = True
	for eachChild in children(parentNode):
		if keyLessThan(disp(eachChild), firstCut(cutSet)) and keyLessThanOrEqual(lastCut(cutSet), keyAdd(disp(eachChild), width(eachChild))) :
			dontDiveDeeperFlag = False
			cutSetLocal = cloneCutSet(cutSet)
			for i, eachCutLocal in enumerate(cutSetLocal):
				cutSetLocal[i] = keySubtract(eachCutLocal, disp(eachChild) )
			recursiveCut(cutSetLocal, eachChild)
		pass
	pass
	if dontDiveDeeperFlag:
		chopUp(cutSet, parentNode)
	iprint('- return recursiveCut', level=-1)
#
def chopUp(cutSet, parentNode):
	iprint("- chopUp(", cutSet, ', ' , parentNode.shortDesc(), ')', level=1)
	for eachCut in cutSet:
		for eachChild in children(parentNode):
			iprint('- eahChild ', eachCut , '  ' , eachChild.shortDesc() )
			if keyLessThan(disp(eachChild), eachCut) and keyLessThanOrEqual(eachCut, keyAdd(disp(eachChild), width(eachChild))):
				newChildSet = split(eachCut, parentNode)
				disown(parentNode, eachChild)
				adopt(parentNode, leftChild(newChildSet))
				adopt(parentNode, rightChild(newChildSet))
				break
		pass
	pass 
	iprint('- return chopUp', level=-1)

#
def split(cutPoint, node):
	iprint("- split(", cutPoint, ', ' , node.shortDesc(), ')', level=1)
	assert(nodeType(node) == NODE_UPPER)
	leftNode = createNewNode()
	rightNode = createNewNode()
	# disp, width calcs are tenuous if we a using non-multivalued storage.
	# could possibly end up in a place with no data. should be renormalized?
	setDisp(leftNode, disp(node))
	setWidth(leftNode, keySubtract(cutPoint, disp(node)))
	setDisp(rightNode, cutPoint)
	setWidth(rightNode, keySubtract(keyAdd(width(node), disp(node)), cutPoint) )
	for eachChild in children(node):
		iprint("- splitchild: ", eachChild.shortDesc(), disp(eachChild) , cutPoint ,  keyAdd(disp(eachChild), width(eachChild)))
		if keyLessThanOrEqual(keyAdd(disp(eachChild), width(eachChild)), cutPoint) :
			adopt(leftNode, eachChild)
		elif keyLessThanOrEqual(cutPoint, disp(eachChild)) :
			adopt(rightNode, eachChild)
		else:
			newChildSet = split(keySubtract(cutPoint, disp(eachChild)), eachChild)
			adopt(leftNode, leftChild(newChildSet))
			adopt(rightNode, rightChild(newChildSet))
	#
	# Normalize, so the sub-trees are internally consistent.
	# this may break the intent
	normalizeDisps(leftNode)
	normalizeDisps(rightNode)
	iprint('- return split', level=-1)
	return makeChildSet(leftNode, rightNode)



#######################################################
# You may not want to use recombination if you're tree
# node sharing.
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

#
#
# No child overflow checks here either.
# take trhew childreen of sibling 1 and 2 and mak them children of parentNode
#
def prmitiveRecombine(parentNode, sibling1, sibling2):
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
