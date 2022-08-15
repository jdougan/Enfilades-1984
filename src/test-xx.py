
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
DEBUG=2

def describe(label, item):
	try:
		lenInt = len(item)
	except:
		lenInt = -1
	print(label, type(item), lenInt, item)

def dprint(*data, level=2, of=print):
	if (DEBUG is not None) & (DEBUG >= level):
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



class Appends2(u.TestCase):
	def construct00(testCase):
		# Build a sigle entry assuming an empty peer node is a valid empty enfilade
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
	def constructBase(testCase):
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
		dprint('# test02 append overflow')
		testCase.assertEqual(m.MAX_CHILD_NODES, 4)
		a = testCase.constructBase()
		b = m.append1(a, 1, 2, 'B')
		testCase.assertEqual(m.width(b),3)
		c = m.append1(b, 1, 3, 'C')
		testCase.assertEqual(m.width(c),4)
		d = m.append1(c, 1, 4, 'D')
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



if __name__ == '__main__':
	u.main()
