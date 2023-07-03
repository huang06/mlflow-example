# MLflow Demo

model versioning is a critical challenge in the Machine Learning lifecycle. It often occurs incompatibility issue when deploying new versions of models.

The aim of this repo is try to solve this kind of issues with MLflow.

Why MLflow? MLflow is famous Python package to track ML experiments and it adds the **model registry** feature since v1.4.0 where we can manage, version and keep lineage of the models.

We first choose MLflow to conduct a POC to manage the GenForecast Models to demonstrate its feasibility.

```text
                                                      --meta data--> PostgreSQL (port 15432)
Client (Python SDK) <--> MLflow Sever (port 5001) <--|
                                                      --artifacts--> MinIO (port 9000, 9001)
```

## Features

- MLflow: tracks the experiments and stores the models in the model registry.
- MinIO: A S3-compatible storge that stores the MLflow artifacts.
- PostreSQL: Stores the MLflow tracking data.

## Prerequsities

- Docker Compose V2
- Python3 (tested with 3.10.12)
- Available ports:
  - 5001 (for mlflow server)
  - 5050 (for pgadmin) (optional)
  - 15432 (for PostgreSQL)
  - 9000, 9001 (for MinIO)

## MLflow Steps

1. genearte a model and wrap it to a wrapped pyfunc.
1. run `mlflow.pyfunc.log_model` to upload the model to artifact storage.
1. run `mlflow.register_model` to register the model in the model registry.
1. run `client.transition_model_version_stage` to transition the model to another stage, such as `Production`.

## Usage

Launch backend containers.

```bash
docker compose -f docker-compose-storage.yaml up -d
```

Set up Python environment.

```bash
rm -r .venv || exit 0
python3 -m pip install pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev -v
```

Launch a MLflow server.

```bash
pipenv shell
export MLFLOW_S3_ENDPOINT_URL="http://127.0.0.1:9000"

pipenv run mlflow server \
  --port 5001 \
  --host 0.0.0.0 \
  --backend-store-uri "postgresql+psycopg2://postgres:postgres@127.0.0.1:15432/mlflow" \
  --default-artifact-root "s3://my-mlflow"
```

Run the training script.

```bash
pipenv shell
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin
export MLFLOW_S3_ENDPOINT_URL="http://127.0.0.1:9000"
python3 train.py
```
