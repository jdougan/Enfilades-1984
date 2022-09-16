#
# tests for the enfilade from the grant and the corrected verions
# This is a scratch areea to develop new twests
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


if __name__ == '__main__':
	u.main()
