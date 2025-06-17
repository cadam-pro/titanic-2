"""
Load, preprocess, prepare, and save the Titanic dataset.
"""
import os
import pandas as pd
from prefect import task, flow
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from titanic.registry import load_model, save_model
from sklearn.model_selection import train_test_split
from titanic.params import DATA_FOLDER,NUMERIC_FEATURES,CAT_FEATURES,DATA_URL

@task
def load_data() -> pd.DataFrame:
    """
    Load the Titanic dataset from a CSV file.
    
    Returns:
        DataFrame: The loaded Titanic dataset.
    """
    return pd.read_csv(DATA_URL,index_col='PassengerId')

@task  
def clean_data(df):
    """
    clean the Titanic dataset.
    
    Args:
        df (DataFrame): The Titanic dataset.
        
    Returns:
        DataFrame: The preprocessed Titanic dataset.
    """
    
    return    df.drop(columns=['Name', 'Ticket', 'Cabin'])\
                .dropna()\
                .drop_duplicates()
      
@task
def prepare_data(df:pd.DataFrame ,fit=True, survive=True) -> tuple[pd.DataFrame, pd.Series]: 
    """
    Prepare the Titanic dataset for training.
    
    Args:
        df (DataFrame): The cleaned Titanic dataset.
        
    Returns:
        tuple: A tuple containing [X,y] the features DataFrame and the target Series.
    """
    if survive:
        X,y = df.drop(columns=['Survived']), df['Survived']
    else:
        X, y = df, None
    if fit :
        numeric_transformer = Pipeline(steps=[
                                            ('imputer', SimpleImputer(strategy='mean')),
                                            ('scaler', StandardScaler())
                                        ])  
        cat_pipeline = Pipeline(steps=[
                                            ('imputer', SimpleImputer(strategy='most_frequent')),
                                            ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first'))
                                        ])
        preprocessor = ColumnTransformer(
                                            transformers=[
                                                ('num', numeric_transformer, NUMERIC_FEATURES),
                                                ('cat', cat_pipeline, CAT_FEATURES)
                                            ],
                                            remainder='passthrough'  # Keep other columns as they are
                                        ).set_output(transform="pandas")
        preprocessor.fit(X)
        save_model(preprocessor, "preprocessor.pkl")
    else:
        preprocessor = load_model("preprocessor.pkl")
    X_scaled = preprocessor.transform(X)
    return X_scaled, y

@task
def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)


@flow(log_prints=True)
def data_workflow():
    df = load_data()
    print(df.shape)
    df = clean_data(df)
    X, y = prepare_data(df)
    print(X.head())
    print(y.head())
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    data_workflow()