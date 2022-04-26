import numpy as np 

def data_split(df, start, end, target_date_col="Date"):
    """
    split the dataset into training or testing using date
    :param data: (df) pandas dataframe, start, end
    :return: (df) pandas dataframe
    """
    data = df[(df[target_date_col] >= start) & (df[target_date_col] < end)]
    data = data.sort_values([target_date_col, "tic"], ignore_index=True)
    data.index = data[target_date_col].factorize()[0]
    return data

def data_split_short_term(df, test_pct, target_date_col="Date"):
    """
    split the dataset into training or testing using date
    :param data: (df) pandas dataframe, start, end
    :return: (df) pandas dataframe
    """
    num = len(df) // test_pct
    num_tickers = len(np.unique(df.tic))
    # Subtract so that df_train & df_test are divisible by num_tickers
    num2 = num - (num % num_tickers)

    df_train = df[:-num2]
    df_train.index =  df_train[target_date_col].factorize()[0]
    df_test = df[-num2:]
    df_test.index =  df_test[target_date_col].factorize()[0]

    return df_train, df_test