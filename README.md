# py-nocodb

Python client for NocoDB API v2


## Install

Install from [pypi](https://pypi.org/project/nocodb-api/):

```shell
pip install nocodb-api
```

Install from Github:

```shell
pip install "nocodb-api@git+https://github.com/infeeeee/py-nocodb"
```

## Quickstart

```python
from nocodb import NocoDB

noco = NocoDB(url="https://app.nocodb.com", api_key="superapikey")

base = noco.get_base("ple9j3sg0j3ks6m")

table = base.get_table_by_title("Sample Views")

[print(i, r.metadata) for i,r in enumerate(table.get_records())]
```

Get debug log:

```python
import logging
from nocodb import NocoDB

logging.basicConfig()
logging.getLogger('nocodb').setLevel(logging.DEBUG)
# Now every log is visible.

# Limit to submodules:
logging.getLogger('nocodb.Base').setLevel(logging.DEBUG)
```


## Development

```shell
python -m venv .venv
. ./.venv/bin/activate
```

### Tests in Docker

Create a file `test_config.json` with the parameters, or change the Environment Variables in `tests/Dockerfile`, than run:

```shell
docker run --rm -it $(docker build -q -f tests/Dockerfile .)
```

### Official docs

- https://meta-apis-v2.nocodb.com
- https://data-apis-v2.nocodb.com
- https://docs.nocodb.com

### Documentation with [pdoc](https://pdoc.dev)

*TODO*

```shell
pip install -e ".[doc]"
pdoc -d google nocodb
```
