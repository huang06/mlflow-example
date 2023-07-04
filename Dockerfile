FROM docker.io/library/python:3.10.12-slim-buster
RUN python3 -m pip install "mlflow[extras]==2.4.1" "psycopg2-binary==2.9.6"
