import pytest
from whsa.utils import parse_name


def test_simple_name():
    name = 'Doe, John'
    d = parse_name(name)
    assert d['last_name'] == 'Doe'
    assert d['first_name'] == 'John'
    assert d['middle_name'] is None
    assert d['suffix'] is None


def test_middle_name():
    name = 'Trump, Ivanka M.'
    d = parse_name(name)
    assert d['middle_name'] == 'M.'
    assert d['last_name'] == 'Trump'
    assert d['first_name'] == 'Ivanka'
    assert d['suffix'] is None

def test_suffix():
    name = 'Kennedy, Jr., John'
    d = parse_name(name)
    assert d['suffix'] == 'Jr.'
    assert d['last_name'] == 'Kennedy'
    assert d['first_name'] == 'John'
    assert d['middle_name'] == None


def test_all_name_parts():
    name = 'Miranda Bob, IV, Lin-Manuel Z.'
    d = parse_name(name)
    assert d['suffix'] == 'IV'
    assert d['last_name'] == 'Miranda Bob'
    assert d['first_name'] == 'Lin-Manuel'
    assert d['middle_name'] == 'Z.'

def test_middle_name_not_initial():
    name = "Doe, John hey-there dude"
    d = parse_name(name)

    assert d['middle_name'] is None
    assert d['first_name'] == 'John hey-there dude'
    assert d['last_name'] == 'Doe'

def test_invalid_names():
    bad_names = ('Jon Doe', 'kladsf', 'doe,jon', 'a,b,c', "Jane-Smith")
    for n in bad_names:
        assert parse_name(n) == {}
