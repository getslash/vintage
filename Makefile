default: test

test: env
	.env/bin/pytest -x tests

env: .env/.up-to-date

doc: env
	.env/bin/sphinx-build -a -W -E doc build/sphinx/html

.env/.up-to-date: pyproject.toml
	python -m venv .env
	.env/bin/pip install -e '.[testing,doc]'
	touch $@

