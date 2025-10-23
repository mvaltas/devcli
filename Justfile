@test *options: format
  uv run pytest {{options}}

@lint:
  uv run black . --check --diff --color

@format:
  uv run black .

@update:
  uv sync --upgrade

@build:
  uv build --wheel

@install: build
  pipx install --force dist/devcli*.whl

@check: install
  devcli example ping
  -devcli show-version
  -devcli show-config

@bundle:
  cd docs; bundle

@docs: bundle
  cd docs; rake
