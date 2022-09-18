#
# tests for the enfilade from the grant and the corrected verions
# This is a scratch area to develop new tests
# Note that a lot of the test debug output is Markdown formatted
#
# This file uses tabs to indent
#
import unittest as u
#import multi as m
m =  __import__("enfilade-grant")

SHOULD_DUMP=True
DEBUG=2
DEFAULT_DPRINT_LEVEL = 2

def describe(label, item):
	try:
		lenInt = len(item)
	except:
		lenInt = -1
	print(label, type(item), lenInt, item)

def dprint(*data, level=DEFAULT_DPRINT_LEVEL, of=print):
	if (DEBUG is not None) and (DEBUG >= level):
		of(*data)

def dumptxt(enfilade, should=None):
	if should is None:
		s = SHOULD_DUMP
	else:  
		s = should
	if s :
		m.dump(enfilade, of=print)

def dump(enfilade, should=None,label=''):
	if should is None:
		s = SHOULD_DUMP
	else:
		s = should
	if s:
		dumpdata = ['*']
		def mdprint(*data):
			for each in data:
				dumpdata.append(str(each))
		m.dump(enfilade, of=mdprint)
		print(' '.join(dumpdata))

def dumpPretty(enfilade, should=None,label=''):
	if should is None:
		s = SHOULD_DUMP
	else:
		s = should
	if s:
		m.dumpPretty(enfilade)

def dumpmd(enfilade, should=None,label=''):
	if should is None:
		s = SHOULD_DUMP
	else:
		s = should
	if s:
		dumpdata = ['*']
		def mdprint(*data):
			for each in data:
				dumpdata.append(str(each))
		m.dump(enfilade, of=mdprint)
		print(' '.join(dumpdata))


class GrantTestsCase(u.TestCase):
	#
	def dprintTestHeader(testCase, methodStr):
		dprint()
		dprint('#', (type(testCase).__name__), methodStr)
	#
	def retrieveCheck1(testCase,enf,start,end):
		# Generate a ordered proplist showing the sequence contents of the enfilade
		# in the specified INCLUSIVE range
		# FIXME canonicalize the domain output so it can be compared in a test
		arr = []
		for i in range(start,end+1) :
			try:
				each = m.retrieveAllIntoList(enf,i,list())
			except Exception as ex:
				each = 'ERROR' + str(type(ex))
			arr.append(i)
			arr.append(each)
		return arr
	#
	def retrieveCheck2(testCase,enf,start,end):
		arr = []
		for i in range(start,end+1) :
			try:
				each = m.retrieve(enf,i)
			except Exception as ex:
				each = 'ERROR' + str(type(ex))
			arr.append(i)
			arr.append(each)
		return arr
	#
	def linearAppendToTail(testCase,startIndex):
		def charForIndex(i):
			return chr(65 + i - startIndex)
		#dprint()
		top = None
		#dprint("APPEND5-INIT", startIndex, 0, charForIndex(startIndex))
		top = m.append(top, startIndex , 0, charForIndex(startIndex))
		last = startIndex + 0
		for i in range(startIndex+1,startIndex+26):
			#dprint()
			#dprint("APPEND5", last, 1, charForIndex(i))
			top = m.append(top, last , 1, charForIndex(i))
			last = last + 1
			# dprint()
			# dumpPretty(top)
			# dprint()
			# dprint("    ",testCase.retrieveCheck1(top,0,27))
		return top
	#
	def linearAppendToFirst(testCase):
		things = []
		indexes = []
		i = 0
		for each in range(65,65+26):
			things.append(chr(each))
			indexes.append(i)
			i = i + 1
		top = None
		for each in indexes:
			top = m.append(top, 1, each, things[each])
		return top

#comment out tests by making them inherit frm object
class AppendsBase(object):
	def construct00(testCase):
		# Build a sigle entry assuming an empty upper node is a valid empty enfilade
		# 2022-09-13 jdougan Not working at present as we are
		# assming an empty Upper Node is an error
		empty = m.createNewNode()
		m.setDisp(empty, m.keyZero())
		m.setWidth(empty, m.keyZero())
		one = m.append(empty, 1, m.keyZero() , 'A')
		return one
	def constructViaAppendFromEmpty(testCase):
		# Build single entry using the support in append
		e2 = m.append(None, m.keyZero(), 1, 'A')
		return e2
	def constructSingleBottomNode(testCase):
		# Build single entry as a single bottom node
		d = 'A'
		b = m.createNewBottomNode()
		m.setData(b, d)
		m.setWidth(b, m.naturalWidth(d))
		m.setDisp(b,1)
		return b
	def constructSingleUpperAndBottomNode(testCase):
		# Build a single entry with an upper node with one bottom node
		b = testCase.constructSingleBottomNode()
		u = m.createNewNode()
		m.adopt(u,b)
		m.setDisp(u, m.keyZero())
		m.setWidth(u, m.calculateWidth(m.children(u)))
		return u


class Appends2(AppendsBase):
	def constructBase(testCase):
		# Build single entry using the support in append
		return testCase.constructViaAppendFromEmpty()
	def test00(testCase):
		dprint()
		dprint('# test00 base construct')
		a = testCase.constructBase()
		dprint(a)
		dumpmd(a)
	def test01(testCase):
		dprint()
		dprint('# test01 append 1,0')
		a = testCase.constructBase()
		b = m.append(a, 1, m.keyZero(), 'B')
		testCase.assertEqual(m.width(b), 1)
		dprint(b)
		dumpmd(b)
	def test02(testCase):
		dprint()
		dprint('# test02 append 1,2')
		a = testCase.constructBase()
		b = m.append(a, 1, 2, 'B')
		testCase.assertEqual(m.width(b),3)
		dprint(b)
		dumpmd(b)
	def test03(testCase):
		dprint()
		dprint('# test03 append overflow')
		testCase.assertEqual(m.MAX_CHILD_NODES, 4)
		a = testCase.constructBase()
		b = m.append(a, 1, 2, 'B')
		testCase.assertEqual(m.width(b),3)
		c = m.append(b, 1, 3, 'C')
		testCase.assertEqual(m.width(c),4)
		d = m.append(c, 1, 4, 'D')
		dumpmd(d)
		testCase.assertEqual(m.width(d),5)
		# it shoud be splitting the node here.
		e = m.append(d, 1, 5, 'E')
		dprint(e)
		dumpmd(e)
		testCase.assertEqual(m.width(e),6)


class Appends3(AppendsBase):
	def constructBase(testCase):
		return testCase.constructViaAppendFromEmpty()
	def test03(testCase):
		dprint()
		dprint('#', (type(testCase).__name__), ' test03 append overflow')
		testCase.assertEqual(m.MAX_CHILD_NODES, 4)
		a = m.append(None, 1, 0, 'A')
		dumpmd(a)
		dprint("===",testCase.retrieveCheck1(a,1,10))
		b = m.append(a, 1, 1, 'B')
		dumpmd(b)
		dprint("===",testCase.retrieveCheck1(b,1,10))
		#testCase.assertEqual(m.width(b),3)
		c = m.append(b, 1, 2, 'C')
		dumpmd(c)
		dprint("===",testCase.retrieveCheck1(c,1,10))
		#testCase.assertEqual(m.width(c),4)
		dprint()
		d = m.append(c, 1, 3, 'D')
		dumpmd(d)
		dprint("===",testCase.retrieveCheck1(d,1,10))
		#testCase.assertEqual(m.width(d),5)
		# it shoud be splitting the node here.
		dprint()
		try:
			m.DEBUG=None
			e = m.append(d, 1, 4, 'E')
		finally:
			m.DEBUG=None
		dumpmd(e)
		#m.setWidth(e,5)
		dprint("===",testCase.retrieveCheck1(e,1,10))
		dprint("-=-=-=-=-=-=-=")
		try:
			m.DEBUG = None
			dprint(m.retrieveAllIntoList(d,4,list()))
			dprint(m.retrieveAllIntoList(e,4,list()))
		finally:
			m.DEBUG = None
		#testCase.assertEqual(m.width(e),6)


class KeyIndexTests(object):
	# Keys/indexes do not have to be comutative
	# distributive makes no sense here
	def associativity(testCase,a,b,c):
		r1 = m.keyAdd(m.keyAdd(a,b),c)
		r2 = m.keyAdd(a,m.keyAdd(b,c))
		testCase.assertTrue(m.keyEquals(r1,r2))
	def invertibility(testCase, a,b ):
		r1 = m.keyAdd(a,b)
		r2 = m.keySubtract(r1,b)
		testCase.assertTrue(m.keyEquals(a,r2))
	def identity(testCase,a):
		r1 = m.keyAdd(a,m.keyZero())
		testCase.assertTrue(m.keyEquals(r1,a))
		r2 = m.keySubtract(a,m.keyZero())
		testCase.assertTrue(m.keyEquals(r2,a))
	def comparators(testCase,a,b):
		# If we use something other than integers, the initial
		# assert will have to be changed
		assert(a < b)
		#
		r1 = m.keyLessThan(a,a)
		testCase.assertFalse(r1)
		r2 = m.keyLessThanOrEqual(a,a)
		testCase.assertTrue(r2)
		r3 = m.keyEquals(a,a)
		testCase.assertTrue(r3)
		#
		r4 = m.keyEquals(a,b)
		testCase.assertFalse(r4)
		r5 = m.keyEquals(b,a)
		testCase.assertFalse(r5)
		r6 = m.keyLessThan(a,b)
		testCase.assertTrue(r6)
		r7 = m.keyLessThan(b,a)
		testCase.assertFalse(r7)
		r8 = m.keyLessThanOrEqual(a,b)
		testCase.assertTrue(r8)
		r9 = m.keyLessThanOrEqual(b,a)
		testCase.assertFalse(r9)
		#
	def test00Properties(testCase):
		testCase.dprintTestHeader("test00Properties")
		# a must be strictly less than b
		data = (
			(10,20,30),
			(1,2,30),
			(-10,20,-10),
			(10,20,30),
			(10,20,30),
			(10,20,30),
			(10,20,30),
			(10,20,30),
			(10,20,30),
			(10,20,30),
			)
		for each in data:
			a = each[0]
			b = each[1]
			c = each[2]
			testCase.comparators(a,b)
			testCase.associativity(a,b,c)
			testCase.invertibility(a,b)
			testCase.identity(a)

class EnwidifyTests(object):
	def assertBounds1(testCase,ds,expected):
		bs = m.NodesBoundsSum()
		for each in ds:
			bs.addDsp(each)
			bs.addDsp(m.keyAdd(each,1))
		testCase.assertEqual(bs.width(), expected)
	def assertBoundsWids(testCase,ds,expected):
		bs = m.NodesBoundsSum()
		for each in ds:
			bs.addDsp(each[0])
			bs.addDsp(m.keyAdd(each[0],each[1]))
		testCase.assertEqual(bs.width(), expected)
	#
	def test00Single(testCase):
		testCase.dprintTestHeader('test00Single')
		ds = [1, 2, 3, 4]
		testCase.assertBounds1(ds, 4)
	def test01Single(testCase):
		testCase.dprintTestHeader('test01Single')
		ds = [1, 4]
		testCase.assertBounds1(ds, 4)
	def test05Wids(testCase):
		testCase.dprintTestHeader('test05Wids')
		ds = [[1,1], [2,1], [3,1], [4,10]]
		testCase.assertBoundsWids(ds, 13)
	def test05Wids(testCase):
		testCase.dprintTestHeader('test06Wids')
		ds = [[1,1], [2,1], [3,11], [4,1]]
		testCase.assertBoundsWids(ds, 13)


class DepthTests(object):
	# I have no idea how this counts in xu88
	def test00EmptyTree(testCase):
		b = None
		testCase.assertEqual(m.depth(b),0)
	def test01BottomNode(testCase):
		b = m.createOneValueEnfiladeBottom(10,'A')
		testCase.assertEqual(m.depth(b),1)
	def test02UpperBottomNode(testCase):
		b = m.createOneValueEnfiladeUpperBottom(10,'A')
		testCase.assertEqual(m.depth(b),2)
	def test03UpperBottomNode(testCase):
		a = m.createOneValueEnfiladeBottom(10,'A')
		b = m.createOneValueEnfiladeBottom(20,'B')
		c = m.normalizeDisps(m.levelPush(a,b))
		testCase.assertEqual(m.depth(c),2)
	def test04UpperBottomNode(testCase):
		a = m.createOneValueEnfiladeUpperBottom(10,'A')
		b = m.createOneValueEnfiladeUpperBottom(20,'B')
		c = m.normalizeDisps(m.levelPush(a,b))
		testCase.assertEqual(m.depth(c),3)

class TraversalTests(GrantTestsCase):
	def test00travtail(testCase):
		testCase.dprintTestHeader("test00travtail")
		out = list()
		top = testCase.linearAppendToTail(1)
		dumpPretty(top)
		def addTuple(node):
			out.append(node)
		m.breadthTraverseNodes(top, addTuple)
		testCase.assertIs(top, out[0])
		print(len(out))
		print(out)
		out=list()
		m.depthTraverseNodes(top, addTuple)
		testCase.assertIs(top, out[-1])
		print(len(out))
		print(out)

	def test05travhead(testCase):
		testCase.dprintTestHeader("test05travhead")
		out = set()
		top = testCase.linearAppendToFirst()
		def addTuple(*args):
			out.add(args)
		m.breadthTraverseNodes(top, addTuple)
		dumpPretty(top)
		print(len(out))
		print(out)
		out=set()
		m.depthTraverseNodes(top, addTuple)
		print(len(out))
		print(out)

	def test10travtailvalues(testCase):
		testCase.dprintTestHeader("test10travtailvalues")
		out = list()
		top = testCase.linearAppendToTail(1)
		m.traverseValuesIntoList(top, out)
		dumpPretty(top)
		print(len(out))
		print(out)

	def test11travtailvalues(testCase):
		testCase.dprintTestHeader("test11travtailvalues")
		out = list()
		top = testCase.linearAppendToTail(1)
		def thingy(data, key, node):
			print(data,key)
		m.traverseValuesFn(top, thingy)
		dumpPretty(top)
		print(len(out))
		print(out)









if __name__ == '__main__':
	u.main()
