import pandas as pd
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