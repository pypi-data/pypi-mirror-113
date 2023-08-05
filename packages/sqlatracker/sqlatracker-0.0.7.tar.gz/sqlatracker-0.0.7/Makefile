env:
	pip3 install pre-commit
	pre-commit install
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate \
	&& pip3 install -r requirements_dev.txt
