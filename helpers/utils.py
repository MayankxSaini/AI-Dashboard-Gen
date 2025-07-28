def apply_filters(df, filters):
    """
    Apply column-wise filters to the DataFrame.

    Parameters:
    - df: pandas DataFrame
    - filters: dict with {column_name: filter_value}

    Returns:
    - filtered DataFrame
    """
    for col, value in filters.items():
        if value != "All" and col in df.columns:
            df = df[df[col] == value]
    return df
