import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache import Cache

def test_cache():
    c = Cache()

    # c.data should be a dict
    assert isinstance(c.data, dict)

    c.put('a', 'foo')
    c.put('b', {'b-a': 'foo'})
    # should be able to put stuff
    assert c.data == {'a': 'foo', 'b': {'b-a': 'foo'}}

    # manually set cache the bad way
    c.data = { 'test_get': 'success' }
    get_data = c.get('test_get')
    # should be able to fetch stuff
    assert get_data == c.data['test_get']

    # manually set cache the bad way
    c.data = { 'test_delete': 'success' }
    c.delete('test_delete')
    # should be able to delete stuff
    assert c.data == {}

    c.data = { 'Nerd': 'present!' }
    ferris = c.check('Bueller')
    perfect_attendance = c.check('Nerd')
    # check should return true if the key is present else false
    assert ferris == False
    assert perfect_attendance == True
