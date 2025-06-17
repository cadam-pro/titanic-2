import mlflow
from prefect import flow, task

@task
def set_mlflow_exp():
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("titanic_experiment")

@task
def mlflow_run(model, X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test) 
        # Log parameters and metrics
        # mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        # Log the model
        mlflow.sklearn.log_model(model, "model", input_example=X_train.head(1))

# @task
# def load_best_model():


@flow
def mlflow_workflow(model, X_train, y_train, X_test, y_test):
    set_mlflow_exp()
    mlflow_run(model, X_train, y_train, X_test, y_test)