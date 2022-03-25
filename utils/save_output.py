import datetime
from config import config
import os

SAVE_DIR = '/Users/minjunpark/Documents/RLfinance/saved_models'
DATA_SAVE_DIR = "datasets"
TRAINED_MODEL_DIR = "trained_models"
TENSORBOARD_LOG_DIR = "tensorboard_log"
RESULTS_DIR = "results"

from utils.fetch_args import fetch_args
config = fetch_args()

# Create directory if it doesn't exist
def create_dir():    
    if not os.path.exists(f"{SAVE_DIR}/{config.currentTime}"):
        os.makedirs(f"{SAVE_DIR}/{config.currentTime}")
        os.makedirs(f"{SAVE_DIR}/{config.currentTime}/{DATA_SAVE_DIR}")
        os.makedirs(f"{SAVE_DIR}/{config.currentTime}/{TRAINED_MODEL_DIR}")
        os.makedirs(f"{SAVE_DIR}/{config.currentTime}/{TENSORBOARD_LOG_DIR}")
        os.makedirs(f"{SAVE_DIR}/{config.currentTime}/{RESULTS_DIR}")

# Save trained model
def save_model(trained_model, model_name):
    trained_model.save(f'{SAVE_DIR}/{TRAINED_MODEL_DIR}/{model_name}')

def save_to_csv(file, filename):
    file.to_csv(f"{SAVE_DIR}/{RESULTS_DIR}/{filename}")
