from whsa.wrangle import get_president

def test_trump():
    for yr in ('2017', '2018', '2019'):
        assert get_president(yr) == 'Trump'


def test_obama():
    for yr in ('2012', '2013', '2014', '2015', '2016', ):
        assert get_president(yr) == 'Obama'
