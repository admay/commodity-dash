import pandas as pd

def gen_df():
    df = pd.read_csv("./test-data.csv")
    df.columns = df.columns.map(lambda col: col.upper())
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEAR'], df['MONTH'], df['DAY'] = df['DATE'].dt.year, df['DATE'].dt.month, df['DATE'].dt.day
    return df

