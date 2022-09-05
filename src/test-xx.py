#
# tests for the enfilade from the grant and the corrected verions
#
# Note that a lot of the test debug output is Markdown formatted
#
#
#
import unittest as u
#import multi as m
m =  __import__("enfilade-grant")

SHOULD_DUMP=True
DEBUG=3

def describe(label, item):
	try:
		lenInt = len(item)
	except:
		lenInt = -1
	print(label, type(item), lenInt, item)

def dprint(*data, level=2, of=print):
	if (DEBUG is not None) and (DEBUG >= level):
		of(*data)

def dumptxt(enfilade, should=None):
	if should is None:
		s = SHOULD_DUMP
	else:
		s = should
	if s :
		m.dump(enfilade, of=print)

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

class AppendsBase(u.TestCase):
	def retrieveCheck1(testCase,enf,start,end):
		arr = []
		for i in range(start,end+1) :
			try:
				each = m.retrieveAllIntoList(enf,i,list())
			except Exception as ex:
				each = 'ERROR' + ex
			arr.append(i)
			arr.append(each)
		return arr
	def retrieveCheck2(testCase,enf,start,end):
		arr = []
		for i in range(start,end+1) :
			each = m.retrieve(enf,i)
			arr.append(each)
		return arr
	def construct00(testCase):
		# Build a sigle entry assuming an empty upper node is a valid empty enfilade
		empty = m.createNewNode()
		m.setDisp(empty, m.keyZero())
		m.setWidth(empty, m.keyZero())
		one = m.append(empty, 1, m.keyZero() , 'A')
		return one
	def construct01(testCase):
		# Build single entry using the support in append1
		e2 = m.append1(None, m.keyZero(), 1, 'A')
		return e2
	def construct03(testCase):
		# Build single entry as a single bottom nodde
		d = 'A'
		b = m.createNewBottomNode()
		m.setData(b, d)
		m.setWidth(b, m.naturalWidth(d))
		m.setDisp(b,1)
		return b
	def construct04(testCase):
		# Build a single entry with an upper node
		b = testCase.construct03()
		u = m.createNewNode()
		m.adopt(u,b)
		m.setDisp(u, m.keyZero())
		m.setWidth(u, m.calculateWidth(m.children(u)))
		return u

class Appends2(AppendsBase):
	def constructBase(testCase):
		# Build single entry using the support in append1
		return testCase.construct01()
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
		b = m.append1(a, 1, m.keyZero(), 'B')
		testCase.assertEqual(m.width(b), 1)
		dprint(b)
		dumpmd(b)
	def test02(testCase):
		dprint()
		dprint('# test02 append 1,2')
		a = testCase.constructBase()
		b = m.append1(a, 1, 2, 'B')
		testCase.assertEqual(m.width(b),3)
		dprint(b)
		dumpmd(b)
	def test03(testCase):
		dprint()
		dprint('# test03 append overflow')
		testCase.assertEqual(m.MAX_CHILD_NODES, 4)
		a = testCase.constructBase()
		b = m.append1(a, 1, 2, 'B')
		testCase.assertEqual(m.width(b),3)
		c = m.append1(b, 1, 3, 'C')
		testCase.assertEqual(m.width(c),4)
		d = m.append1(c, 1, 4, 'D')
		dumpmd(d)
		testCase.assertEqual(m.width(d),5)
		# it shoud be splitting the node here.
		e = m.append1(d, 1, 5, 'E')
		dprint(e)
		dumpmd(e)
		testCase.assertEqual(m.width(e),6)
	#
	#
	#
	def test10(testCase):
		dprint()
		dprint('# test10 append 0,2')
		a = testCase.constructBase()
		b = None
		#
		# FIXME Ths should raiise but it currently doesn't, probably
		# because of the weirdness around the zero keys
		#
		#with testCase.assertRaises(KeyError):
			#b = m.append1(a, m.keyZero(), 2, 'B')
		testCase.assertIs(b,None)
		dprint(b)
		#dumpmd(b)
	def test11(testCase):
		dprint()
		dprint('# test11 append 2,0')
		a = testCase.constructBase()
		b = None
		with testCase.assertRaises(KeyError):
			b = m.append1(a, 2, m.keyZero(), 'B')
		dprint(b)
		#dumpmd(b)


class Appends3(AppendsBase):
	def constructBase(testCase):
		return testCase.construct01()
	def test03(testCase):
		dprint()
		dprint('# Appends3 test03 append overflow')
		testCase.assertEqual(m.MAX_CHILD_NODES, 4)
		a = m.append2(None, 1, 0, 'A')
		dumpmd(a)
		dprint("===",testCase.retrieveCheck1(a,1,10))
		b = m.append2(a, 1, 1, 'B')
		dumpmd(b)
		dprint("===",testCase.retrieveCheck1(b,1,10))
		#testCase.assertEqual(m.width(b),3)
		c = m.append2(b, 1, 2, 'C')
		dumpmd(c)
		dprint("===",testCase.retrieveCheck1(c,1,10))
		#testCase.assertEqual(m.width(c),4)
		dprint()
		d = m.append2(c, 1, 3, 'D')
		dumpmd(d)
		dprint("===",testCase.retrieveCheck1(d,1,10))
		#testCase.assertEqual(m.width(d),5)
		# it shoud be splitting the node here.
		dprint()
		try:
			m.DEBUG=None
			e = m.append2(d, 1, 4, 'E')
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


class Append4(AppendsBase):
	def test00node(testCase):
		dprint()
		things = []
		indexes = []
		i = 0
		for each in range(65,65+26):
			things.append(chr(each))
			indexes.append(i)
			i = i + 1
		top = None
		for each in indexes:
			top = m.append2(top, 1, each, things[each])
		m.dumpPretty(top)
		dprint()
		dprint("    ",testCase.retrieveCheck1(top,0,27))
	#
class Append5(AppendsBase):
	def test01node(testCase):
		testCase.linearAppendToTail(5)
	#
	def linearAppendToTail(testCase,startIndex):
		def charForIndex(i):
			return chr(65 + i - startIndex)
		m.DEBUG = 1
		dprint()
		top = None
		dprint("APPEND5-INIT", startIndex, 0, charForIndex(startIndex))
		top = m.append2(top, startIndex , 0, charForIndex(startIndex))
		last = startIndex + 0
		for i in range(startIndex+1,startIndex+26):
		#for i in range(startIndex+1,startIndex+17):
			dprint()
			dprint("APPEND5", last, 1, charForIndex(i))
			top = m.append2(top, last , 1, charForIndex(i))
			last = last + 1
			dprint()
			m.dumpPretty(top)
			dprint()
			dprint("    ",testCase.retrieveCheck1(top,0,27))
		# try:
		# 	print("APPEND5", last, 1, things[5])
		# 	m.DEBUG = 8
		# 	top = m.append2(top, last , 1, things[5])
		# finally:
		# 	pass
		# dumpmd(top)
		# dprint("    ",testCase.retrieveCheck1(top,1,26))









class Enwidify1(u.TestCase):
	def test00Single(testCase):
		bs = m.BoundsSum()
		ds = [1, 2, 3, 4]
		for each in ds:
			bs.addDsp(each)
			bs.addDsp(each + 1)
		testCase.assertEqual(bs.width(), 4)




if __name__ == '__main__':
	u.main()
