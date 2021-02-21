environment.yaml:
	conda env export --no-builds > environment.yaml
.PHONY: environment.yaml

tests:
	python -m pytest tests/
.PHONY: tests