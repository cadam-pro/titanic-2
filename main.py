"""

"""

from titanic.data import data_workflow
from titanic.registry import save_model
from titanic.train import train_workflow
from titanic.mlflow import mlflow_workflow


def train():
    # data= load_data(train=True)
    # data = clean_data(data)
    X_train, X_test, y_train, y_test = data_workflow()
    model = train_workflow(X_train, y_train)
    mlflow_workflow(model, X_train, y_train, X_test, y_test)
    
if __name__ == "__main__":
    train()
