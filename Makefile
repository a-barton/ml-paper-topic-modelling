CONTAINER_NAME?=ml-paper-topic-modelling

environment.yaml:
	conda env export --no-builds > environment.yaml
.PHONY: environment.yaml

tests:
	python -m pytest tests/
.PHONY: tests

container:
	sudo docker build --tag $(CONTAINER_NAME) .

local-serve:
	sudo docker run -p 5000:5000 -it ml-paper-topic-modelling

heroku-login:
	sudo heroku login

heroku-create: heroku-login
	sudo heroku create $(CONTAINER_NAME)

heroku-container-login: heroku-login
	sudo heroku container:login

heroku-container-push: heroku-login heroku-container-login
	sudo heroku container:push web

heroku-container-release: heroku-login heroku-container-login heroku-container-push
	sudo heroku container:release web