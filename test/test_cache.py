import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import Cache

def test_cache():
    c = Cache()

    # c.data should be a dict
    assert isinstance(c.table, dict)
    assert isinstance(c.graph, dict)

    c.put('table', 'a', 'foo')
    c.put('table', 'b', {'b-a': 'foo'})
    # should be able to put stuff
    assert c.table == {'a': 'foo', 'b': {'b-a': 'foo'}}

    # manually set cache the bad way
    c.table = {'test_get': 'success'}
    get_data = c.get('table', 'test_get')
    # should be able to fetch stuff
    assert get_data == c.table['test_get']

    c.table = {'Nerd': 'present!'}
    ferris = c.check('table', 'Bueller')
    perfect_attendance = c.check('table', 'Nerd')
    # check should return true if the key is present else false
    assert ferris == False
    assert perfect_attendance == True
