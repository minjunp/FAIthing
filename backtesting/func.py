import pandas as pd

def calculate_df_account_val(df_actions, baseline):
    """
    Given set of actions taken for each stock, calculate total account value

    Input:
        df_actions: dataframe that contains each actions
        baseline: Initial amount in portfolio

    Output:
        df_account_value: total account value returned for each timepoint

    To do:
        When there's multiple stocks, think about how to achieve this
    """
    account_vals = []
    # Define initial amount
    num = 0 # number of stocks owned
    for i, action in enumerate(df_actions.Actions.values):
        if action > 0:
            baseline -= action * df_actions.Close[i]
            num += action # Total number of particular stocks owned
        elif action < 0:
            baseline += -action * df_actions.Close[i] # Remember action is negative for selling
            num += action
        
        account_val = baseline + (num * df_actions.Close[i])
        account_vals.append(account_val)

    df_account_value = pd.DataFrame({'account_value': account_vals}, index=df_actions.index)

    return df_account_value