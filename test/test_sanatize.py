import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import ffn

from sanatize import sanatize_dataframe, get_headers
from generators import gen_df

def test_sanatize_dataframe():
    df = sanatize_dataframe(gen_df())

    actual_headers = list(df)
    expected_headers = ['DATE', 'AFE_0 A:10_01', 'ANS_0 A:10_01', 'YEAR', 'MONTH', 'DAY']

    # should add YEAR, MONTH, and DAY
    assert actual_headers == expected_headers
    # should capitalize all headers
    assert [x.upper() for x in actual_headers] == actual_headers
    # shouldn't lose data
    assert df.isnull().sum().sum() == 0

def test_get_headers():
    df = gen_df()

    headers = get_headers(df)

    # should drop date related columns
    assert headers == ['AFE_0 A:10_01', 'ANS_0 A:10_01']
