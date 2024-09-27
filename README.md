# py-nocodb

Python client for NocoDB API v2


## Quickstart

```python
from nocodb import NocoDB

noco = NocoDB(url="https://app.nocodb.com", api_key="superapikey")

base = noco.get_base("ple9j3sg0j3ks6m")

table = base.get_table_by_title("Sample Views")

[print(i, r.metadata) for i,r in enumerate(table.get_records())]
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