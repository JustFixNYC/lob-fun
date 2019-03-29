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


def test_is_populated_works():
    assert ParsedAddress('foo', '', '', '').is_populated() is False
    assert ParsedAddress('', 'foo', '', '').is_populated() is False
    assert ParsedAddress('o', 'foo', '1', 'b').is_populated() is True


def test_short_desc_works():
    assert ParsedAddress('foo', '1', '2', '3').short_desc() == "'foo' '1' '2' '3'"


@pytest.mark.parametrize('value,expected', [
    ('Blarg,', 'Blarg'),
    ('Blarg\n', 'Blarg'),
    (['foo', 'bar'], 'foo bar')
])
def test_clean_works(value, expected):
    assert clean(value) == expected
