"""
Train the Titanic model.
"""
import pandas as pd
from prefect import flow, task
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from titanic.registry import save_model

@task
def train_model(X:pd.DataFrame, y:pd.Series) -> LogisticRegression:
    """ 
    Initiate the model and train it on the Titanic dataset.
    Args:
        X (DataFrame): The features DataFrame.
        y (Series): The target Series.
    Returns:
        LogisticRegression: The trained logistic regression model.
    """
    model = LogisticRegression(max_iter=1000, random_state=42
                               ,C=1, penalty='l2', solver='liblinear')
    model.fit(X, y)
    return model

def evaluate_model(  X_test: pd.DataFrame
                   , y_test: pd.Series
                   , model: LogisticRegression) -> float:
    return {"accuracy" : accuracy_score(y_test, model.predict(X_test)),
            "f1_score" : f1_score(y_test, model.predict(X_test)),
            "precision": precision_score(y_test, model.predict(X_test)),
            "recall"   : recall_score(y_test, model.predict(X_test))}

@flow
def train_workflow(X, y):
    model = train_model(X, y)
    save_model(model, "best_model.pkl")
    return model