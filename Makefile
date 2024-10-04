default: test

test: env
	.venv/bin/pytest -x tests

env:
	uv venv
	uv pip install -e ".[testing,doc]"

doc: env
	.venv/bin/sphinx-build -a -W -E doc build/sphinx/html
