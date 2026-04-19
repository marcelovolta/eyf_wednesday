import pandas as pd
from .config import *

def simple_gain_v1(df: pd.DataFrame, prediction_column_name: str, \
                   target_column_name: str) -> float:
    '''
    Calculates gain using economical considerations: cost of marketing action and client lifetime value
    assuming that the eficacy of a marketing action directed to the right person (BAJA+2) has a 50% 
    eficacy, that is 50% of the clients targeted stay as clients. 
    Also, GAIN_CORRECT_PREDICTION and COST_MARKETING_ACTION are defined in the config file using these guidelines
    Finally, this calculation defines 'BAJA+1' and 'BAJA+2' as positive or 1, and 'CONTINUA' as negative or 0
    Other ways of calculating gain need alternative definitions
    Params
    ------
    - df: Pandas Dataframe that contains a prediction, and the traget class (CONTINUA, BAJA+1, BAJA+2)
    Returns
    ------.
    - A float value that contains the gain summed over all rows in the dataframe
    '''
    
    correct_preds = (df[(df[target_column_name]=='BAJA+2') & (df[prediction_column_name]==1)]).sum()
    incorrect_preds = (df[(df[target_column_name]!='BAJA+2') & (df[prediction_column_name]==1)]).sum()
    
    gain = (correct_preds * GAIN_CORRECT_PREDICTION) - (incorrect_preds * COST_MARKETING_ACTION)

    return gain