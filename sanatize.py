import pandas as pd


def sanatize_dataframe(df):
    df.columns = df.columns.map(lambda col: col.upper())
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day
    return df


def get_headers(df):
    return list(df.drop(columns=['DATE', 'YEAR', 'MONTH', 'DAY']))
