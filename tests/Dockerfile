FROM python:3.8-slim-bullseye

WORKDIR /root/nocodb

COPY . .

RUN pip install --no-cache-dir .

# Change envvars here, or create a test_config.json file with these values:
# ENV NOCO_URL=https://app.nocodb.com
# ENV NOCO_API_KEY=apikey
# ENV NOCO_BASE_ID=baseid
# ENV TIMEOUT=30

CMD python -m unittest discover -v -s ./tests -p "test_*.py"

# docker run --rm -it $(docker build -q -f tests/Dockerfile .)
