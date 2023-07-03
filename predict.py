import logging

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://127.0.0.1:5001")
    client = MlflowClient()

    model_name = "ElasticnetWineModel"
    stage = "Production"
    model = mlflow.sklearn.load_model(model_uri=f"models:/{model_name}/{stage}")
    # model = client.get_registered_model(model_name)
    print(model)
