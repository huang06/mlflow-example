# MLflow Demo

This project uses MLflow to track model training experiments and manage model versioning.

We refer to this [document](https://mlflow.org/docs/latest/tracking.html#scenario-4-mlflow-with-remote-tracking-server-backend-and-artifact-stores) to simulate setting up a remote MLflow server, creating a PostgreSQL database to store model information, and set up MinIO to store model artifacts.

```text
                                                      --meta data--> PostgreSQL (port 15432)
Client (Python SDK) <--> MLflow Sever (port 5001) <--|
                                                      --artifacts--> MinIO (port 9000, 9001)
```

## Components

- MLflow: tracks the experiments and stores the models in the model registry.
- MinIO: A S3-compatible storge that stores the MLflow artifacts.
- PostreSQL: Stores the MLflow tracking data.

## Prerequsities

- Docker Compose V2
- Python3 (tested with 3.10)
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

Install Python packages.

```bash
python3 -m pip install pipenv
pipenv install --dev -v
```

Launch backend services.

```bash
docker compose up -d
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

```text
2023/07/03 21:19:30 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2023/07/03 21:19:30 INFO mlflow.store.db.utils: Updating database tables
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 451aebb31d03, add metric step
INFO  [alembic.runtime.migration] Running upgrade 451aebb31d03 -> 90e64c465722, migrate user column to tags
INFO  [alembic.runtime.migration] Running upgrade 90e64c465722 -> 181f10493468, allow nulls for metric values
INFO  [alembic.runtime.migration] Running upgrade 181f10493468 -> df50e92ffc5e, Add Experiment Tags Table
INFO  [alembic.runtime.migration] Running upgrade df50e92ffc5e -> 7ac759974ad8, Update run tags with larger limit
INFO  [alembic.runtime.migration] Running upgrade 7ac759974ad8 -> 89d4b8295536, create latest metrics table
INFO  [89d4b8295536_create_latest_metrics_table_py] Migration complete!
INFO  [alembic.runtime.migration] Running upgrade 89d4b8295536 -> 2b4d017a5e9b, add model registry tables to db
INFO  [2b4d017a5e9b_add_model_registry_tables_to_db_py] Adding registered_models and model_versions tables to database.
INFO  [2b4d017a5e9b_add_model_registry_tables_to_db_py] Migration complete!
INFO  [alembic.runtime.migration] Running upgrade 2b4d017a5e9b -> cfd24bdc0731, Update run status constraint with killed
INFO  [alembic.runtime.migration] Running upgrade cfd24bdc0731 -> 0a8213491aaa, drop_duplicate_killed_constraint
INFO  [alembic.runtime.migration] Running upgrade 0a8213491aaa -> 728d730b5ebd, add registered model tags table
INFO  [alembic.runtime.migration] Running upgrade 728d730b5ebd -> 27a6a02d2cf1, add model version tags table
INFO  [alembic.runtime.migration] Running upgrade 27a6a02d2cf1 -> 84291f40a231, add run_link to model_version
INFO  [alembic.runtime.migration] Running upgrade 84291f40a231 -> a8c4a736bde6, allow nulls for run_id
INFO  [alembic.runtime.migration] Running upgrade a8c4a736bde6 -> 39d1c3be5f05, add_is_nan_constraint_for_metrics_tables_if_necessary
INFO  [alembic.runtime.migration] Running upgrade 39d1c3be5f05 -> c48cb773bb87, reset_default_value_for_is_nan_in_metrics_table_for_mysql
INFO  [alembic.runtime.migration] Running upgrade c48cb773bb87 -> bd07f7e963c5, create index on run_uuid
INFO  [alembic.runtime.migration] Running upgrade bd07f7e963c5 -> 0c779009ac13, add deleted_time field to runs table
INFO  [alembic.runtime.migration] Running upgrade 0c779009ac13 -> cc1f77228345, change param value length to 500
INFO  [alembic.runtime.migration] Running upgrade cc1f77228345 -> 97727af70f4d, Add creation_time and last_update_time to experiments table
INFO  [alembic.runtime.migration] Running upgrade 97727af70f4d -> 3500859a5d39, Add Model Aliases table
INFO  [alembic.runtime.migration] Running upgrade 3500859a5d39 -> 7f2a7d5fae7d, add datasets inputs input_tags tables
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
2023/07/03 21:19:31 INFO mlflow.store.db.utils: Creating initial MLflow database tables...
2023/07/03 21:19:31 INFO mlflow.store.db.utils: Updating database tables
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
[2023-07-03 21:19:31 +0800] [6314] [INFO] Starting gunicorn 20.1.0
[2023-07-03 21:19:31 +0800] [6314] [INFO] Listening at: http://0.0.0.0:5001 (6314)
[2023-07-03 21:19:31 +0800] [6314] [INFO] Using worker: sync
[2023-07-03 21:19:31 +0800] [6315] [INFO] Booting worker with pid: 6315
[2023-07-03 21:19:31 +0800] [6316] [INFO] Booting worker with pid: 6316
[2023-07-03 21:19:31 +0800] [6317] [INFO] Booting worker with pid: 6317
[2023-07-03 21:19:31 +0800] [6318] [INFO] Booting worker with pid: 6318
```

Open a new shell and run the training script.

```bash
pipenv shell
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin
export MLFLOW_S3_ENDPOINT_URL="http://127.0.0.1:9000"
export MLFLOW_TRACKING_URI="http://127.0.0.1:5001"
python3 train.py
```
