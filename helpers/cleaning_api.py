import pandas as pd
import numpy as np

def auto_clean_dataframe(df: pd.DataFrame):
    """
    Automatically clean a DataFrame by:
    - Removing empty rows/columns
    - Dropping duplicates
    - Standardizing column names
    - Dropping rows with >50% missing
    - Converting objects to numeric/datetime where safe
    """
    df = df.copy()

    # Drop fully empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Standardize column names
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    # Drop rows with too many missing values
    df = df.dropna(thresh=int(0.5 * len(df.columns)))

    # Convert object columns to numeric or datetime where possible
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

    return df
