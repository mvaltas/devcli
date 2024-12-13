@test *options: lint
  poetry run pytest {{options}}

@lint:
  poetry run black . --check

@format:
  poetry run black .

@update:
  poetry update

@build:
  poetry build --format=wheel

@install: build
  pipx install --force dist/devcli*.whl

@check: install
  devcli example ping
  -devcli show-version
  -devcli show-config
