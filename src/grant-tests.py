#
# tests for the enfilade from the grant and the corrected verions
#
# Note that a lot of the test debug output is Markdown formatted
#
# This file is indented using tabs
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



##########################################################################
## Tests Below 
##
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



class KeyIndexTests(GrantTestsCase):
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
		# FIXME need more test data
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

class EnwidifyTests(GrantTestsCase):
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



class Building(GrantTestsCase):
	def test01NodeCreation(testCase):
		testCase.dprintTestHeader('test01NodeCreation')
		dprint("## Test BottomNode 1")
		b1 = m.createNewBottomNode()
		m.setData(b1,'A')
		m.setWidth(b1,m.naturalWidth('A'))
		m.setDisp(b1,0)
		dump(b1)
		top = b1
		dprint("## Test BottomNode 2")
		b2 = m.createNewBottomNode()
		m.setData(b2,'B')
		m.setWidth(b2,m.naturalWidth('B'))
		m.setDisp(b2,2)
		dump(b2)
		dprint("## Test Uppper Node")
		b3 = m.createNewNode()
		m.adopt(b3,b1)
		m.adopt(b3,b2)
		m.setWidth(b3, m.calculateWidth(m.children(b3)))
		m.setDisp(b3, 5)
		dump(b3)

def createTestEnfilade00(dsp=m.keyZero()):
	# build  without higher level API
	b1 = m.createNewBottomNode()
	m.setData(b1,'A')
	m.setWidth(b1,m.naturalWidth('A'))
	m.setDisp(b1,0)
	b2 = m.createNewBottomNode()
	m.setData(b2,'B')
	m.setWidth(b2,m.naturalWidth('B'))
	m.setDisp(b2,2)
	b3 = m.createNewNode()
	m.adopt(b3,b1)
	m.adopt(b3,b2)
	m.setWidth(b3,3)
	m.setDisp(b3,dsp)
	return b3

class Levels(GrantTestsCase):
	def test01LevelPush(testCase):
		testCase.dprintTestHeader('test01LevelPush')
		e1 = createTestEnfilade00(1)
		dump(e1)
		e2 = createTestEnfilade00(5)
		dump(e2)
		e3 = m.levelPush(e1,e2)
		dump(e3)
		e4 = m.normalizeDisps(e3)
		dump(e4)
		testCase.assertEqual(m.width(e4), 7)
	def test02LevelPop(testCase):
		testCase.dprintTestHeader('test02LevelPop')
		e1 = createTestEnfilade00(1)
		dump(e1)
		e2 = createTestEnfilade00(5)
		dump(e2)
		e3 = m.normalizeDisps(m.levelPush(e1,e2))
		dump(e3)
		m.disown(e3,e2)
		e4 = m.levelPop(e3)
		testCase.assertIs(e4,e1)

#
#
#
#
#
def createTestEnfilade01():
	b1 = m.createNewBottomNode()
	m.setData(b1,'A')
	m.setWidth(b1,m.naturalWidth('A'))
	m.setDisp(b1,5)
	b2 = m.createNewBottomNode()
	m.setData(b2,'B')
	m.setWidth(b2,m.naturalWidth('B'))
	m.setDisp(b2,7)
	top = b1
	top = m.levelPush(top, b2)
	top = m.normalizeDisps(top)
	return top

def createTestEnfilade02():
	b1 = m.createNewBottomNode()
	m.setData(b1,'A')
	m.setWidth(b1,m.naturalWidth('A'))
	m.setDisp(b1,20)
	b2 = m.createNewBottomNode()
	m.setData(b2,'B')
	m.setWidth(b2,m.naturalWidth('B'))
	m.setDisp(b2,22)
	top = b1
	top = m.levelPush(top, b2)
	top = m.normalizeDisps(top)
	return top

# 
#
#
#
#
class RetrievalsSingle(GrantTestsCase):
	def test01BottomNodeRetrieve(testCase):
		testCase.dprintTestHeader('test01BottomNodeRetrieve')
		top = m.createNewBottomNode()
		m.setData(top,'B')
		m.setWidth(top,m.naturalWidth('B'))
		m.setDisp(top,7)
		data = testCase.retrieveCheck2(top,5,9)
		should = [5, None, 6, None, 7, 'B', 8, None, 9, None]
		testCase.assertEqual(data, should)
	def test02Retrieves(testCase):
		testCase.dprintTestHeader('test02Retrieves')
		top = createTestEnfilade01()
		data = testCase.retrieveCheck2(top,0,10)
		should = [0, None, 1, None, 2, None, 3, None, 4, None, 5, 'A', 6, None, 7, 'B', 8, None, 9, None, 10, None]
		testCase.assertEqual(data, should)
	def test03Retrieves(testCase):
		testCase.dprintTestHeader('test03Retrieves')
		top = createTestEnfilade02()
		data = testCase.retrieveCheck2(top,0,30)
		should = [0, None, 1, None, 2, None, 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9, None, 10, None, 11, None, 12, None, 13, None, 14, None, 15, None, 16, None, 17, None, 18, None, 19, None, 20, 'A', 21, None, 22, 'B', 23, None, 24, None, 25, None, 26, None, 27, None, 28, None, 29, None, 30, None]
		testCase.assertEqual(data, should)
	def test04RetrievesPushed(testCase):
		testCase.dprintTestHeader('test04RetrievesDisp')
		top = createTestEnfilade01()
		a = createTestEnfilade02()
		top= m.normalizeDisps(m.levelPush(top, a))
		data = testCase.retrieveCheck2(top,0,30)
		should = [0, None, 1, None, 2, None, 3, None, 4, None, 5, 'A', 6, None, 7, 'B', 8, None, 9, None, 10, None, 11, None, 12, None, 13, None, 14, None, 15, None, 16, None, 17, None, 18, None, 19, None, 20, 'A', 21, None, 22, 'B', 23, None, 24, None, 25, None, 26, None, 27, None, 28, None, 29, None, 30, None]
		testCase.assertEqual(data, should)
	def test05RetrievesDisped(testCase):
		testCase.dprintTestHeader('test05RetrievesDisped')
		top = createTestEnfilade02()
		m.setDisp(top, m.keySubtract(m.disp(top), 20))
		data = testCase.retrieveCheck2(top,-1,10)
		should = [-1, None, 0, 'A', 1, None, 2, 'B', 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9, None, 10, None]
		testCase.assertEqual(data, should)

class RetrievalsMulti(GrantTestsCase):
	def test01BottomNodeRetrieve(testCase):
		testCase.dprintTestHeader('test01BottomNodeRetrieve')
		top = m.createNewBottomNode()
		m.setData(top,'B')
		m.setWidth(top,m.naturalWidth('B'))
		m.setDisp(top,7)
		data = testCase.retrieveCheck1(top,5,9)
		should = [5, [], 6, [], 7, ['B'], 8, [], 9, []]
		testCase.assertEqual(data, should)
	def test02Retrieves(testCase):
		testCase.dprintTestHeader('test02Retrieves')
		top = createTestEnfilade01()
		data = testCase.retrieveCheck1(top,0,10)
		should = [0, [], 1, [], 2, [], 3, [], 4, [], 5, ['A'], 6, [], 7, ['B'], 8, [], 9, [], 10, []]
		testCase.assertEqual(data, should)
	def test03Retrieves(testCase):
		testCase.dprintTestHeader('test03Retrieves')
		top = createTestEnfilade02()
		data = testCase.retrieveCheck1(top,0,30)
		should = [0, [], 1, [], 2, [], 3, [], 4, [], 5, [], 6, [], 7, [], 8, [], 9, [], 10, [], 11, [], 12, [], 13, [], 14, [], 15, [], 16, [], 17, [], 18, [], 19, [], 20, ['A'], 21, [], 22, ['B'], 23, [], 24, [], 25, [], 26, [], 27, [], 28, [], 29, [], 30, []]
		testCase.assertEqual(data, should)
	def test04RetrievesPushed(testCase):
		testCase.dprintTestHeader('test04RetrievesDisp')
		top = createTestEnfilade01()
		a = createTestEnfilade02()
		top= m.normalizeDisps(m.levelPush(top, a))
		data = testCase.retrieveCheck1(top,0,30)
		should = [0, [], 1, [], 2, [], 3, [], 4, [], 5, ['A'], 6, [], 7, ['B'], 8, [], 9, [], 10, [], 11, [], 12, [], 13, [], 14, [], 15, [], 16, [], 17, [], 18, [], 19, [], 20, ['A'], 21, [], 22, ['B'], 23, [], 24, [], 25, [], 26, [], 27, [], 28, [], 29, [], 30, []]
		testCase.assertEqual(data, should)
	def test05RetrievesDisped(testCase):
		testCase.dprintTestHeader('test05RetrievesDisped')
		top = createTestEnfilade02()
		m.setDisp(top, m.keySubtract(m.disp(top), 20))
		data = testCase.retrieveCheck1(top,-1,10)
		should = [-1, [], 0, ['A'], 1, [], 2, ['B'], 3, [], 4, [], 5, [], 6, [], 7, [], 8, [], 9, [], 10, []]
		testCase.assertEqual(data, should)


class AppendsBase(GrantTestsCase):
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

class ZzAppend1(AppendsBase):
	def test00LinearAppendToFirst(testCase):
		testCase.dprintTestHeader('test00LinearAppendToFirst')
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
		dumpPretty(top)
		data = testCase.retrieveCheck1(top,0,27)
		should = [0, [], 1, ['A'], 2, ['B'], 3, ['C'], 4, ['D'], 5, ['E'], 6, ['F'], 7, ['G'], 8, ['H'], 9, ['I'], 10, ['J'], 11, ['K'], 12, ['L'], 13, ['M'], 14, ['N'], 15, ['O'], 16, ['P'], 17, ['Q'], 18, ['R'], 19, ['S'], 20, ['T'], 21, ['U'], 22, ['V'], 23, ['W'], 24, ['X'], 25, ['Y'], 26, ['Z'], 27, []]
		dprint()
		dprint("    ", data)
		testCase.assertEqual(data, should)
class ZzAppend2(AppendsBase):
	def test00LinearAppendToLastPlus5(testCase):
		testCase.dprintTestHeader('test00LinearAppendToLastPlus5')
		top = testCase.linearAppendToTail(5)
		dumpPretty(top)
		dprint()
		data = testCase.retrieveCheck1(top,0,32)
		dprint("    ", data)
		should = [0, [], 1, [], 2, [], 3, [], 4, [], 5, ['A'], 6, ['B'], 7, ['C'], 8, ['D'], 9, ['E'], 10, ['F'], 11, ['G'], 12, ['H'], 13, ['I'], 14, ['J'], 15, ['K'], 16, ['L'], 17, ['M'], 18, ['N'], 19, ['O'], 20, ['P'], 21, ['Q'], 22, ['R'], 23, ['S'], 24, ['T'], 25, ['U'], 26, ['V'], 27, ['W'], 28, ['X'], 29, ['Y'], 30, ['Z'], 31, [], 32, []]
		testCase.assertEqual(data, should)
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

class Append3(AppendsBase):
	def constructBase(testCase):
		# Build single entry using the support in append
		return testCase.constructViaAppendFromEmpty()
	def test10ValidAppendToSingle(testCase):
		testCase.dprintTestHeader('test10ValidAppendToSingle')
		a1 = testCase.constructBase()
		dump(a1)
		b1 = m.append(a1, 1, m.keyZero(), 'B')
		dump(b1)
	def test11InvalidAppendToSingle(testCase):
		testCase.dprintTestHeader('test11InvalidAppendToSingle')
		a2 = testCase.constructBase()
		dump(a2)
		with testCase.assertRaises(KeyError):
			b2 = m.append(a2, 2, m.keyZero(), 'B')
			# should never print
			dprint("* this should not be reached ", b2)
			dump(b2)



if __name__ == '__main__':
	u.main()
