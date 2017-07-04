

NOSETESTS = nosetests --stop -v --pdb --with-coverage --cover-package=sigfoxapi


all:
	@echo TODO


test:
	$(NOSETESTS) tests/test_object.py tests/test_sigfoxapi.py
