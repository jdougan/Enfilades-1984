#
##
#
#
all: tests

tests: grant-tests.log.md test-xx.log.md

grant-tests.log.md : grant-tests.py enfilade-grant.py
	python grant-tests.py -v > grant-tests.log.md 
test-xx.log.md: test-xx.py enfilade-grant.py
	python test-xx.py > test-xx.log.md
clean :
	rm -f grant-tests.log.md
	rm -f test-xx.log.md


