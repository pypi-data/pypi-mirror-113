create_venv:
	# Create virtual environment.
	python3.8 -m venv venv
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install --upgrade setuptools
	./venv/bin/pip3 install --upgrade wheel
	./venv/bin/pip3 install -r requirements.txt

test:
	# Run pytest.
	./venv/bin/pytest --cov=flask_first tests/

format:
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a
