import pytest

from parseaddrs import parse_address, ParsedAddress, clean


@pytest.mark.parametrize('raw,expected', [
    (
        '150 Court St.\nBrooklyn, NY 11201',
        ParsedAddress('150 Court St.', 'Brooklyn', 'NY', '11201')
    ),
])
def test_parse_address_works(raw, expected):
    assert parse_address(raw) == expected


@pytest.mark.parametrize('value,expected', [
    ('Blarg,', 'Blarg'),
    ('Blarg\n', 'Blarg'),
    (['foo', 'bar'], 'foo bar')
])
def test_clean_works(value, expected):
    assert clean(value) == expected
