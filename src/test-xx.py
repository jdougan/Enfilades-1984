
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
	def construct01(testCase):
		e2 = m.append(None, m.keyZero(), 1, 'A')
		return e2
	def construct00(testCase):
		empty = m.createNewNode()
		m.setDisp(empty, m.keyZero())
		m.setWidth(empty, m.keyZero())
		one = m.append(empty, 1, m.keyZero() , 'A')
		return one
	def construct03(testCase):
		d = 'A'
		b = m.createNewBottomNode()
		m.setData(b, d)
		m.setWidth(b, m.naturalWidth(d))
		m.setDisp(b,1)
		return b
	def construct04(testCase):
		b = testCase.construct03()
		u = m.createNewNode()
		m.adopt(u,b)
		m.setDisp(u, m.keyZero())
		m.setWidth(u, m.calculateWidth(m.children(u)))
		return u
	def constructBase(testCase):
		return testCase.construct04()
	def test00(testCase):
		dprint('# base construct')
		a = testCase.constructBase()
		dprint(a)
		dumpmd(a)
	def test01(testCase):
		dprint('# append 0,2')
		a = testCase.constructBase()
		b = m.append(a, m.keyZero(), 2, 'B')
		dprint(b)
		dumpmd(b)
	def test02(testCase):
		dprint('# append 2,0')
		a = testCase.constructBase()
		b = m.append(a, 2, m.keyZero(), 'B')
		dprint(b)
		dumpmd(b)
	def test03(testCase):
		dprint('# append 1,1')
		a = testCase.constructBase()
		b = m.append(a, 1, m.keyZero(), 'B')
		dprint(b)
		dumpmd(b)
	def test04(testCase):
		dprint('# append 1,0')
		a = testCase.constructBase()
		b = m.append(a, 1, 2, 'B')
		dprint(b)
		dumpmd(b)









if __name__ == '__main__':
	u.main()
