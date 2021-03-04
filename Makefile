APP_NAME?=ml-paper-topic-modelling

init:
	conda create -f environment.yaml -n $(APP_NAME)

environment.yaml:
	conda env export --no-builds > environment.yaml
.PHONY: environment.yaml

container:
	docker build --tag $(APP_NAME) .

local-serve:
	docker run -p 5000:5000 -it ml-paper-topic-modelling

# IN CASE OF "cgroups: cannot find cgroup mount destination" ERROR, RUN THE FOLLOWING:
# sudo mkdir /sys/fs/cgroup/systemd
# sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd
tests: container
	python -m pytest tests/
.PHONY: tests

heroku-login:
	heroku login

heroku-create: heroku-login
	heroku create $(APP_NAME)

heroku-container-login: heroku-login
	heroku container:login

heroku-container-push: heroku-login heroku-container-login
	heroku container:push web

heroku-container-release: heroku-login heroku-container-login heroku-container-push
	heroku container:release web