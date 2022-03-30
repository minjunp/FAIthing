import argparse
from numpy import float64
import datetime

# Needs to be modified...
def fetch_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-tt', '--task_type', type=str, default='epitope', help='Task type')
    parser.add_argument('-ep', '--epoch', type=int, default=10, help='Number of epochs')
    parser.add_argument('-bs', '--batch_size', type=int, default=8, help='Batch size')
    parser.add_argument('-lr', '--learning_rate', type=float64, default=3e-5, help='Optimizer learning rate')
    parser.add_argument('-ws', '--warmup_steps', type=int, default=0, help='Number of warmup steps')


    args = parser.parse_args()
    currentTime = datetime.datetime.now().strftime('%Y%m%d-%Hh')

    args.currentTime = currentTime
    args.SAVE_DIR = '/Users/minjunpark/Documents/RLfinance/saved_models'
    args.DATA_SAVE_DIR = 'datasets'
    args.TRAINED_MODEL_DIR = "trained_models"
    args.TENSORBOARD_LOG_DIR = "tensorboard_log"
    args.RESULTS_DIR = "results"

    args.TRADE_START_DATE = "2015-01-01"
    args.TRADE_END_DATE = "2016-01-01"
    args.BACKTEST_START_DATE = "2015-06-01"

    return args