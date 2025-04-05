import pandas as pd

required_columns = ['timestamp', 'scenario', 'worst_case', 'solution']

def validate_data(df):
    """Ensure the dataset has all the required columns."""
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f'Missing required column: {column}')
    return df