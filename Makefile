install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv power_analysis/test_*.py

format:
	black power_analysis/*.py

lint:
	find power_analysis/ -name "*.py" | xargs pylint --disable=R,C

all: install lint test