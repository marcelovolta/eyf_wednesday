# Core Python
import logging
from operator import ge
import os
import datetime as dt 

# External libraries
import pandas as pd
import polars as pl
import duckdb

# Modular code
from src import * 

# Log setup
os.makedirs('logs', exist_ok=True)
fecha = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_log = f'logs/log_{fecha}.log'
logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s', \
    datefmt='%Y-%m-%d %H:%M:%S', 
    handlers = [logging.FileHandler(nombre_log, mode='w', encoding='utf-8'), \
    logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():

    # Start logging
    logger.info("Start run")
    
    # Get settings from env and yaml
    API_KEY = config.API_KEY
    logger.info(
        f"Bogus API Key just for checking that secrets work: {API_KEY}"
    )
    
    
    logger.info(
        f"""
            Parameters from config - Experiment name: {config.EXPERIMENT_NAME} 
            Seeds: {config.SEEDS} 
            Gain of Correct prediction: {config.GAIN_CORRECT_PREDICTION} 
            Cost of Marketing action: {config.COST_MARKETING_ACTION} 
            Data Paths: {config.DATA_PATHS} 
            Train Months: {config.TRAIN_MONTHS} 
            Test Months: {config.TEST_MONTHS}    
            Validation Months: {config.VALIDATION_MONTHS}
            """
            )
    
    
    # Load the data from the CSV file
    data = load_data_pandas(config.DATA_PATHS)
    

    if data is None: return
    print(data.head())
    print(data.tail())
    
    logging.info(f"Rows: {data.shape[0]}")
    logging.info(f"Columns: {data.shape[1]}")
    
    amount_cols = select_amount_cols(data)
    count_cols = select_count_cols(data)

    if amount_cols is None or count_cols is None:
        logging.error("No amount columns, or no count cols have been found")
        return
    
    logging.info(f"Length of amount column list: {len(amount_cols)}")
    logging.info(f"Length of count column list: {len(count_cols)}")
    cols_for_lag = amount_cols + count_cols
    
    data = generate_ternary_class(data)
    data = convert_ternary_class_to_binary(data, 'clase_ternaria', 'clase_ternaria')
    data = generate_lags(data, cols_for_lag, [1, 2, 3, 6, 12], True)

    logging.info("End run")

    


'''
This is the main function that will be called when the script is run.
Do not allow it to be called from outside this file.
'''
if __name__ == "__main__":
    main()