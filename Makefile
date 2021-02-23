environment.yaml:
	conda env export --no-builds > environment.yaml
.PHONY: environment.yaml

tests:
	python -m pytest tests/
.PHONY: tests

container:
	sudo docker build --tag latest .

local-serve:
	sudo docker run -p 5000:5000 -it latest