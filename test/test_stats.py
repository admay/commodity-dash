import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stats import get_index_stats, create_trace
from generators import gen_df

import ffn

def test_get_index_stats():
    df = gen_df()
    index = list(df)[2]
    stats = get_index_stats(index, df)

    # stats should be an instance of GroupStats
    assert isinstance(stats, ffn.core.GroupStats)

def test_create_trace():
    df = gen_df()
    index = list(df)[2]
    x_data = df['DATE']
    y_data = df[index]

    trace_no_opts = create_trace(x_data, y_data)
    trace_opts = create_trace(x_data, y_data, { 'a': 'foo' }) # opts is arbitrary

    # no opts
    assert trace_no_opts == { 'x': x_data, 'y': y_data }
    # with opts
    assert trace_opts == { 'x': x_data, 'y': y_data, 'a': 'foo' }
