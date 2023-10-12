FROM docker.io/library/python:3.10.13-slim-bookworm
RUN python3 -m pip install "mlflow[extras]==2.7.1" "psycopg2-binary==2.9.9"
