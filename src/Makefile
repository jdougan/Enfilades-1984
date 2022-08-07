#
##
#
#
all: tests

tests: grant-tests.log.md

grant-tests.log.md : grant-tests.py enfilade-grant.py
	python grant-tests.py -v > grant-tests.log.md 

clean :
	rm grant-tests.log.md

