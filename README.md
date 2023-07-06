# MLflow Example

This project uses MLflow to track model training experiments and manage artifacts.

We refer to [Scenario 5](https://mlflow.org/docs/latest/tracking.html#scenario-5-mlflow-tracking-server-enabled-with-proxied-artifact-storage-access) to set up a remote MLflow server as proxy server, creating a PostgreSQL database to store model information, and set up MinIO to store model artifacts.

## Components

- MLflow: tracks the experiments and stores the models in the model registry.
- MinIO: A S3-compatible storge that stores the MLflow artifacts.
- PostgreSQL: Stores the MLflow tracking data.

## Prerequsities

- Docker Compose V2
- Python3 (tested with 3.10)
- Available ports:
  - 5001 (for mlflow server)
  - 15432 (for PostgreSQL)
  - 9000, 9001 (for MinIO)

## Usage

Install Python packages.

```bash
python3 -m pip install pipenv
pipenv install
```

Launch MLflow services.

```bash
docker compose build mlflow
docker compose up -d
```

Run the examples.

```bash
pipenv shell

export MLFLOW_TRACKING_URI="http://127.0.0.1:5001"

python3 train.py
# python3 predict.py
```

### MLflow model metadata

The MLflow pyfunc wraps the model instance and metadata. Let's see the metadata structure.

```python
from pprint import pprint
import mlflow
import pandas as pd

model_path = 'runs:/afe88a44e0374bf4bf6221225d382bd6/model'
loaded_model = mlflow.pyfunc.load_model(model_path)
pprint(loaded_model.metadata.to_dict())
```

```python
{'artifact_path': 'model',
 'flavors': {'python_function': {'env': {'conda': 'conda.yaml',
                                         'virtualenv': 'python_env.yaml'},
                                 'loader_module': 'mlflow.sklearn',
                                 'model_path': 'model.pkl',
                                 'predict_fn': 'predict',
                                 'python_version': '3.10.12'},
             'sklearn': {'code': None,
                         'pickled_model': 'model.pkl',
                         'serialization_format': 'cloudpickle',
                         'sklearn_version': '1.3.0'}},
 'mlflow_version': '2.4.1',
 'model_uuid': 'dc8f7048c7114d2d888cde838581406c',
 'run_id': 'afe88a44e0374bf4bf6221225d382bd6',
 'signature': {'inputs': '[{"type": "double", "name": "fixed acidity"}, '
                         '{"type": "double", "name": "volatile acidity"}, '
                         '{"type": "double", "name": "citric acid"}, {"type": '
                         '"double", "name": "residual sugar"}, {"type": '
                         '"double", "name": "chlorides"}, {"type": "double", '
                         '"name": "free sulfur dioxide"}, {"type": "double", '
                         '"name": "total sulfur dioxide"}, {"type": "double", '
                         '"name": "density"}, {"type": "double", "name": '
                         '"pH"}, {"type": "double", "name": "sulphates"}, '
                         '{"type": "double", "name": "alcohol"}]',
               'outputs': '[{"type": "tensor", "tensor-spec": {"dtype": '
                          '"float64", "shape": [-1]}}]'},
 'utc_time_created': '2023-07-06 02:12:50.210345'}
```

### Cleanup

```bash
# close services
docker compose down -v

# delete Python venv
pipenv --rm
```

## Misc

### MLflow ERD

![ERD](docs/erd.png)
