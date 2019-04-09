import pandas as pd

def validate_csv(csv):
    return true

def sanatize_dataframe(df):
    df.columns = df.columns.map(lambda col: col.upper())
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEAR'], df['MONTH'], df['DAY'] = df['DATE'].dt.year, df['DATE'].dt.month, df['DATE'].dt.day
    return df

def get_headers(df):
    headers = list(df)
    headers.remove('DATE')
    return headers
