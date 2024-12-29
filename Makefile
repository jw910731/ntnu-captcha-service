.PHONY: all dev test 

all: dev

dev:
	poetry run fastapi dev src/ntnu_captcha_service/route.py

test:
	poetry run pytest

