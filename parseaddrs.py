import json
from typing import NamedTuple, List, Tuple, Iterator, Union
from collections import OrderedDict
from pathlib import Path
import usaddress


MY_DIR = Path(__file__).parent.resolve()
LANDLORDS_JSON = MY_DIR / 'landlords.json'


class ParsedAddress(NamedTuple):
    line_1: str
    city: str
    state: str
    zipcode: str

    def is_populated(self) -> bool:
        for value in self:
            if not value:
                return False
        return True


class LandlordParseResult(NamedTuple):
    raw_address: str
    is_looked_up: bool
    parsed_address: ParsedAddress


def clean(value: Union[List[str], str]) -> str:
    if isinstance(value, list):
        value = ' '.join(value)
    value = value.strip()
    if value.endswith(','):
        value = value[:-1]
    return value


def parse_address(raw: str) -> ParsedAddress:
    parts: List[Tuple[str, str]] = usaddress.parse(raw)
    line_1_parts: List[str] = []
    city_parts: List[str] = []
    state_parts: List[str] = []
    zipcode = ''
    for value, kind in parts:
        if kind == 'PlaceName':
            city_parts.append(value)
        elif kind == 'StateName':
            state_parts.append(value)
        elif kind == 'ZipCode':
            assert zipcode == ''
            zipcode = value
        else:
            line_1_parts.append(value)
    return ParsedAddress(
        line_1=clean(line_1_parts),
        city=clean(city_parts),
        state=clean(state_parts),
        zipcode=clean(zipcode)
    )


def parse_landlord_addresses() -> Iterator[LandlordParseResult]:
    landlords = json.loads(LANDLORDS_JSON.read_text())
    for landlord in landlords:
        assert landlord['model'] == 'loc.landlorddetails'
        fields = landlord['fields']
        raw_address = fields['address']
        if not raw_address:
            continue

        parsed_address = parse_address(raw_address)
        pa = LandlordParseResult(
            raw_address=raw_address,
            is_looked_up=fields['is_looked_up'],
            parsed_address=parsed_address,
        )
        yield pa


if __name__ == '__main__':
    total = 0
    for addr in parse_landlord_addresses():
        total += 1
        print(repr(addr.raw_address), addr.is_looked_up)
        parsed = json.dumps(addr.parsed_address)
        print(f"  {parsed}")
    print(f"{total} total addresses.")
