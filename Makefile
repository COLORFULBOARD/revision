
install:
	pip install -q .

install-dev:
	pip install -q -e .[dev]

lint:
	flake8 . --exclude=.tox,tests

test:
	@tox
