import pytest
from pysrc.utils import foo
from pysrc import __version__

def test_foo():
    assert foo() == 'foo'

def test_version_number_is_in_alignment():
    assert __version__ == '0.0.1'
