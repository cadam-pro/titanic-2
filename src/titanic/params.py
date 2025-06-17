import os

DATA_FOLDER= "data"
MODEL_FOLDER = os.environ.get("MODEL_FOLDER"
                              , "models")
CAT_FEATURES = ["Embarked", "Sex"]
NUMERIC_FEATURES = ["Age", "Fare"]

DATA_URL = "https://storage.googleapis.com/schoolofdata-datasets/titanic-train.csv"