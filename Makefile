default: test

test: env
	.env/bin/py.test -x tests

env: .env/.up-to-date

doc: env
	.env/bin/python setup.py build_sphinx -a -E


.env/.up-to-date: setup.py
	virtualenv .env
	.env/bin/pip install -e .
	.env/bin/pip install pytest -r doc/pip_requirements.txt
	touch $@

