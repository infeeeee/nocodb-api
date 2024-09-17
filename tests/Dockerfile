FROM python:3.9-slim-bullseye

WORKDIR /root/nocodb

COPY . .

RUN pip install --no-cache-dir .

CMD python -m unittest discover -v -s ./tests -p "test_*.py"

# docker run --rm -it $(docker build -q -f tests/Dockerfile .)