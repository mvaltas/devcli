@test *options:
  poetry run pytest {{options}}

@lint:
  poetry run black . --check

@format:
  poetry run black .

@build:
  poetry build --format=wheel

@install: build
  pipx install --force dist/devcli*.whl

@check: install
  devcli example ping
  -devcli show-version
