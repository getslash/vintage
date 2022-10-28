default: test

test: env
	.env/bin/pytest -x tests

env: .env/.up-to-date

doc: env
	.env/bin/python setup.py build_sphinx -a -E

.env/.up-to-date: setup.py pyproject.toml
	python -m venv .env
	.env/bin/pip install -e '.[testing,doc]'
	touch $@

