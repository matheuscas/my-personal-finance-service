test:
	python -Wonce::DeprecationWarning -Im pytest --cov="." --cov-report=html -n auto
