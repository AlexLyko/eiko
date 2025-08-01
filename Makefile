install:
	pip install -r requirements.txt
test:
	pytest tests
api_dev:
	python efastapi.py
api_prod:
	python main.py 