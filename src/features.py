import pandas as pd
from pandas.api.types import is_numeric_dtype
import duckdb
import logging

logger = logging.getLogger(__name__)

def select_amount_cols(df: pd.DataFrame) -> list[str] | None:
    '''
    Selects amount columns taking into account that these are identified by means
    of a "m" prefix in the column name, e.g.: "mcuenta_corriente"

    Args
    ----
        df: A Pandas DataFrame where the columns will be selected

    Returns
    -------
        List of strings or None
    '''
    if df.empty or df is None:
        logger.error("No dataframe provided or dataframe is empty")
        return None
    
    amount_cols = []
    for col in df.columns:
        if col.startswith('m'):
            amount_cols.append(col)
    return amount_cols

def select_count_cols(df: pd.DataFrame) -> list[str] | None:
    '''
    Selects count columns taking into account that these are identified by means
    of a "c" prefix in the column name, e.g.: "cplazo_fijo"

    Args
    ----
        df: A Pandas DataFrame where the columns will be selected

    Returns
    -------
        List of strings or None
    '''
    if df.empty or df is None:
        logger.error("No dataframe provided or dataframe is empty")
        return None
    
    count_cols = []
    for col in df.columns:
        if col.startswith('c'):
            count_cols.append(col)
    logger.info(f"Count columns: {count_cols}")
    return count_cols

def generate_ternary_class(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Generates the ternary class that signals clients who will churn in 1, or 2
    months, or else they will ocntinue being clients beyond 2 months from the 
    current month
    Args
    ----
        - df: Pandas DataFrame where the ternary class needs to be added

    Returns
    -------
        - A Pandas DataFrame with the new column added. Ancillary columns like this one
        have an underscore prefix
    '''


    logger.info(
        f"Generating ternary class. Starting DataFrame has {df.shape[1]} columns"
    )
    
    sql = '''
          WITH data_source AS (
            SELECT dataset.*, 
            LEAD(foto_mes, 1, NULL) OVER (PARTITION by numero_de_cliente ORDER BY foto_mes) AS lead_1,
            LEAD(foto_mes, 2, NULL) OVER (PARTITION by numero_de_cliente ORDER BY foto_mes) AS lead_2
            FROM dataset
          )  
          SELECT ds.* EXCLUDE (lead_1, lead_2),
          CASE WHEN ds.lead_1 IS NULL AND ds.lead_2 IS NULL THEN 'BAJA+1'
          WHEN ds.lead_1 IS NOT NULL AND ds.lead_2 IS NULL THEN 'BAJA+2'
          ELSE 'CONTINUA'
          END AS _clase_ternaria
          FROM data_source AS ds
        '''
    
    
    conn = duckdb.connect(database=":memory:")
    conn.register("dataset", df)
    df_return = conn.execute(sql).df()
    conn.close()

    logger.info(
        f"Ternary class generation complete. Resulting DataFrame has {df_return.shape[1]} columns"
    )

    baja_1 = (df_return['clase_ternaria']=='BAJA+1').sum()
    baja_2 = (df_return['clase_ternaria']=='BAJA+2').sum()
    continua = (df_return['clase_ternaria']=='CONTINUA').sum()
    logger.info(
        f"Distribution - BAJA+1: {baja_1}, BAJA+2: {baja_2}, CONTINUA: {continua}"
    )

    df_return.head()
    return df_return


def generate_lags(df: pd.DataFrame, columns: list[str], lags: list[int], generate_deltas: bool) \
    -> pd.DataFrame:
    """
    Create lag features for the given columns and lags using SQL

    Args:
    -----
        df: Pandas.DataFrame. The dataframe to create lags for
        columns: List of strings. The columns to create lags for
        lags: List of integers. The lags to create

    Returns:
    --------
        Pandas DataFrame with the lags created
    """
    
    logger.info(f"Creating lags for the following columns: {columns} with the following lags: {lags}")
    
    sql = "SELECT dataset.*"
    for col in columns:
        if is_numeric_dtype(df[col]):
            for lag in lags:
                sql += f", LAG({col}, {lag}) OVER (PARTITION BY numero_de_cliente ORDER BY foto_mes) \
                    AS {col}_lag_{lag}"
                if generate_deltas:
                    sql += f", {col} - {col}_lag_{lag} AS {col}_deltalag_{lag}"
    sql += " FROM dataset"
    
    # for column in columns:
    #     for lag in lags:
    #         df[f"{column}_lag_{lag}"] = df[column].shift(lag)
    # return df

    # We use this method where we receive a dataframe, create the connection
    # and then create a new dataframe that will replace the old one in the calling
    # function. In this way we avoid tying calls together. We look for idempotency
    # The con created here is destroyed once this functions ends executing

    conn = duckdb.connect(database=":memory:")
    conn.register("dataset", df)
    df = conn.execute(sql).df()
    conn.close()

    logger.info(
        f"Lag generation complete. Resulting DataFrame has {df.shape[1]} columns"
    )

    return df

def convert_ternary_class_to_binary(df: pd.DataFrame, ternary_class_column_name: str, \
    binary_class_column_name: str) -> pd.DataFrame:
    '''
    Converts the ternary class to binary so that it can be used as target for training
    Args
    ----
        - df: Pandas Dataframe where the transformation should be done
        - ternary_class_column_name: Name of the column used for ternary class
        - binary_class_column_name: Name of the new column that contains the binary class
        If you set the same name for ternary and binary then the column is replaced
    Returns
    -------
        Pandas dataframe with a new binary class
    '''

    logger.info("Conversion of ternary class into bynary class for use as a target")
    return_df = df.copy()
    baja_1_count = (return_df[ternary_class_column_name] == 'BAJA+1').sum()
    baja_2_count = (return_df[ternary_class_column_name] == 'BAJA+2').sum()
    continua_count = (return_df[ternary_class_column_name] == 'CONTINUA').sum()
    
    return_df[binary_class_column_name] = return_df[ternary_class_column_name].map(
        {
            'CONTINUA': 0,
            'BAJA+1': 1, 
            'BAJA+2': 1
         }
    )

    zero_values = (return_df[binary_class_column_name] == 0).sum()
    one_values = (return_df[binary_class_column_name] == 1).sum()
    logger.info(
        f"""
        Original Ternary class distribution: 
            - BAJA+1: {baja_1_count}, {(baja_1_count/return_df.shape[0])*100:.2f}%
            - BAJA+2: {baja_2_count}, {(baja_2_count/return_df.shape[0])*100:.2f}%
            - CONTINUA: {continua_count}, {(continua_count/return_df.shape[0])*100:.2f}%
        Resulting target count
          - 0: {zero_values}, {(zero_values/(zero_values + one_values))*100:.2f}%
          - 1: {one_values}, {(one_values/(zero_values + one_values))*100:.2f}%  
        """
    )

    return return_df