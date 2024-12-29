REGISTRY?=registry.h.jw910731.dev/nix
IMAGE=ntnu-captcha-service
VERSION=0.1.0

TAG=$(REGISTRY)/$(IMAGE):$(VERSION)

.PHONY: all dev test docker 

all: dev

dev:
	poetry run fastapi dev src/ntnu_captcha_service/route.py

test:
	poetry run pytest

docker-build:
	docker build . --tag $(TAG)