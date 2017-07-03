

NOSETESTS = nosetests -s -v --pdb --with-coverage --cover-package=sigfoxapi


all:
	@echo TODO


test:
	$(NOSETESTS) tests/test_objasdict.py
