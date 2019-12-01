import pytest
from whsa.utils import cleanspaces
from whsa.fuse import cleansalary


def test_cleanspaces_strips():
    name = '   Doe, John '
    assert cleanspaces(name) == 'Doe, John'

def test_cleanspaces_squeezes():
    name = ' Doe,   John   C'
    assert cleanspaces(name) == 'Doe, John C'


def test_cleansalary_removes_commas_and_dollar_signs():
    sal = "$999,823.22"
    assert cleansalary(sal) == '999823.22'

def test_cleansalary_strips():
    sal = "   $1,000 "
    assert cleansalary(sal) == '1000'
