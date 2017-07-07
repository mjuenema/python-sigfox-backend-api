

NOSETESTS = nosetests --stop -v --pdb --with-coverage --cover-package=sigfoxapi --with-id


all:
	@echo TODO


test:
	$(NOSETESTS) tests/test_object.py tests/test_sigfoxapi.py

test_failed:
	$(NOSETESTS) --failed tests/test_object.py tests/test_sigfoxapi.py
