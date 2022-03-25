# Import libraries
from src.env_stocktrading import StockTradingEnv
from models.models import DRLAgent

"""
Input:
    df_test: pd.DataFrame
    trained_model: from Trainer
    env_kwargs: RL environment setting
--------------------
Return: 
    df_account_value: change in account balance over testing time
    df_actions: Actions taken based on learned policy & iteration
"""
class Evaluator():
    def __init__(self, df_test, trained_model, env_kwargs):
        self.df_test = df_test
        self.trained_model = trained_model
        self.env_kwargs = env_kwargs

    def eval_func(self):
        # Testing for held-out data
        e_trade_gym = StockTradingEnv(df = self.df_test, **self.env_kwargs)
        # env_trade, obs_trade = e_trade_gym.get_sb_env()
        df_account_value, df_actions = DRLAgent.DRL_prediction(
        model = self.trained_model, 
        environment = e_trade_gym)

        return df_account_value, df_actions
