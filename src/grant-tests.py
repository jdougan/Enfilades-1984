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

SHOULD_DUMP=False
DEBUG=2

def describe(label, item):
	try:
		lenInt = len(item)
	except:
		lenInt = -1
	print(label, type(item), lenInt, item)

def dprint(*data, level=2):
	if (DEBUG is not None) & (DEBUG >= level):
		print(*data)

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

class AABuilding(u.TestCase):
	def test01NodeCreation(testCase):
		dprint("# Building.testNodeCreation")
		dprint("## Test BottomNode 1")
		b1 = m.createNewBottomNode()
		m.setData(b1,'A')
		m.setWidth(b1,m.naturalWidth('A'))
		m.setDisp(b1,5)
		dump(b1)
		top = b1
		dprint("## Test BottomNode 2")
		b2 = m.createNewBottomNode()
		m.setData(b2,'B')
		m.setWidth(b2,m.naturalWidth('B'))
		m.setDisp(b2,7)
		dump(b2)
		dprint("## Test Uppper Node")
		b3 = m.createNewNode()
		m.adopt(b3,b1)
		m.adopt(b3,b2)
		m.setWidth(b3, m.calculateWidth(m.children(b3)))
		m.setDisp(b3, m.keyZero())
		dump(b3)

def createTestEnfilade00(dsp=m.keyZero()):
	# build  without higher level API
	b1 = m.createNewBottomNode()
	m.setData(b1,'A')
	m.setWidth(b1,m.naturalWidth('A'))
	m.setDisp(b1,5)
	b2 = m.createNewBottomNode()
	m.setData(b2,'B')
	m.setWidth(b2,m.naturalWidth('B'))
	m.setDisp(b2,7)
	b3 = m.createNewNode()
	m.adopt(b3,b1)
	m.adopt(b3,b2)
	m.setWidth(b3,3)
	m.setDisp(b3,dsp)
	return b3

class BALevels(u.TestCase):
	def test01LevelPush(testCase):
		dprint('# Levels.textLevelPush')
		e1 = createTestEnfilade00(0)
		dump(e1)
		e2 = createTestEnfilade00(5)
		dump(e2)
		e3 = m.levelPush(e1,e2)
		dump(e3)
		testCase.assertEqual(m.width(e3), 8)
	def test02LevelPop(testCase):
		dprint('# Levels.textLevelPop')
		e1 = createTestEnfilade00(0)
		dump(e1)
		e2 = createTestEnfilade00(5)
		dump(e2)
		e3 = m.levelPush(e1,e2)
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
	return top

# 
#
#
#
#
class CARetrievalsSingle(u.TestCase):
	pass

class DARetrievalsMulti(u.TestCase):
	RetrieveFns = [m.retrieveAllIntoGrant, m.retrieveAllInto , 'm.retrieveAllInto2']
	RetrieveFnLabels = ['retrieveAllIntoGrant', 'retrieveAllInto', 'retrieveAllInto2']	
	def commonRetrieve(testCase, top, fn, fnLabel, shouldOffset=0):
		should = ['[]', '[]', '[]', '[]', '[]', 'A', '[]', 'B', '[]', '[]', '[]']
		dprint('##', fnLabel)
		for key in range(3,10):
			res = set()
			try:
				dprint('###', key)
				fn(top, key, res)
			except Exception as err:
				dprint('* FAILED', key, err)
			dprint('*',key,should[key-1],res)
			dprint()
	def test01BottomNodeRetrieve(testCase):
		dprint("# Retrievals.testBottomNodeRetrieve")
		b2 = m.createNewBottomNode()
		m.setData(b2,'B')
		m.setWidth(b2,m.naturalWidth('B'))
		m.setDisp(b2,7)
		dprint(b2)
		dump(b2)
		dprint(6, '[]', m.retrieveAllInto(b2,6,set()))
		dprint(7, 'B',  m.retrieveAllInto(b2,7,set()))
	def test02Retrieves(testCase):
		dprint('# Retrievals.testRetrieves')
		top = createTestEnfilade01()
		for i in range(0,2):
			testCase.commonRetrieve(top, testCase.RetrieveFns[i], testCase.RetrieveFnLabels[i])
	def test03RetrievesDisp(testCase):
		dprint('# Retrievals.testRetrievesDisp')
		top = createTestEnfilade01()
		m.setDisp(top,1)
		for i in range(0,2):
			testCase.commonRetrieve(top, testCase.RetrieveFns[i], testCase.RetrieveFnLabels[i],shouldOffset=1)

class EAAppends(u.TestCase):
	def test01Append(testCase):
		dprint('# Appends.testAppend')
		dprint('## t1')
		t1 = createTestEnfilade01()
		dump(t1)
		dprint()
		dprint('## t2')
		t2 = m.append(t1, 7, 100, 'C')
		dump(t1)
		dump(t2)
		dprint()
		dprint('## t3')
		t3 = m.append(t2, 6, 200, 'D ')
		dump(t1)
		dump(t2)
		dump(t3)
		dprint()
		dprint('## t4')
		t4 = m.append(t3, 5, 200, 'E')
		dump(t1)
		dump(t2)
		dump(t3)
		dump(t4)
		dprint()
		dprint('## t5')
		t5 = m.append(t4, 7, 50, 'F')
		dump(t1)
		dump(t2)
		dump(t3)
		dump(t4)
		dump(t5)
		dprint()


if __name__ == '__main__':
	u.main()
