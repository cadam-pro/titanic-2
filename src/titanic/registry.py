"""
Save and load models, preprocessors
"""
import os
import pickle

from prefect import task
from titanic.params import MODEL_FOLDER

def ensure_model_folder():
    """
    Ensure that the model folder exists.
    """
    if not os.path.exists(MODEL_FOLDER):
        os.makedirs(MODEL_FOLDER+"s")
ensure_model_folder() 

@task
def save_model(model, path: str):
    """
    Save a model to the specified path.
    
    Args:
        model: The model to save.
        path (str): The file path where the model will be saved.
    """
    final_path = os.path.join(MODEL_FOLDER, path)
    with open(final_path, 'wb') as f:
        pickle.dump(model, f)

def load_model(path: str):
    """
    Load a model from the specified path.
    
    Args:
        path (str): The file path from which the model will be loaded.
        
    Returns:
        The loaded model.
    """
    final_path = os.path.join(MODEL_FOLDER, path)
    with open(final_path, 'rb') as f:
        model = pickle.load(f)
    return model