import datetime
from config import config
import os

from utils.fetch_args import fetch_args
config = fetch_args()

# Create directory if it doesn't exist
def create_dir():    
    if not os.path.exists(f"{config.SAVE_DIR}/{config.currentTime}"):
        os.makedirs(f"{config.SAVE_DIR}/{config.currentTime}")
        os.makedirs(f"{config.SAVE_DIR}/{config.currentTime}/{config.DATA_SAVE_DIR}")
        os.makedirs(f"{config.SAVE_DIR}/{config.currentTime}/{config.TRAINED_MODEL_DIR}")
        os.makedirs(f"{config.SAVE_DIR}/{config.currentTime}/{config.TENSORBOARD_LOG_DIR}")
        os.makedirs(f"{config.SAVE_DIR}/{config.currentTime}/{config.RESULTS_DIR}")

# Save trained model
def save_model(trained_model, model_name):
    trained_model.save(f'{config.SAVE_DIR}/{config.currentTime}/{config.TRAINED_MODEL_DIR}/{model_name}')

def save_to_csv(file, filename):
    file.to_csv(f"{config.SAVE_DIR}/{config.currentTime}/{config.RESULTS_DIR}/{filename}")
