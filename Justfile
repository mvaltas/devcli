test *options:
  DEVCLI_LOGLEVEL=debug uv run pytest {{options}}

lint:
 uv run black . --check --diff --color

format:
 uv run black .

update:
 uv sync --upgrade

build:
 uv build --wheel

install: clean build
 pipx install --force dist/devcli*.whl

check: install
 devcli example ping
 -devcli show-version
 -devcli show-config

bundle:
 cd docs; bundle

docs: bundle
  cd docs; rake

clean:
  rm -f dist/devcli*.whl

@run +commands:
  - uv run python bin/devcli {{commands}}
