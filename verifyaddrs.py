import os
import sys
import json
from typing import Dict, Any, Optional
import pickle
import lob
from dotenv import load_dotenv

from parseaddrs import parse_landlord_addresses, ParsedAddress, MY_DIR

CACHE_PATH = MY_DIR / '.lob-cache'

load_dotenv()

lob.api_key = os.environ['LOB_API_KEY']

Verification = Dict[str, Any]

VerificationMap = Dict[ParsedAddress, Verification]

_vmap: Optional[VerificationMap] = None


def get_verification(addr: ParsedAddress) -> Verification:
    if not addr.is_populated():
        raise ValueError('Address must be fully populated')
    v = lob.USVerification.create(
        primary_line=addr.line_1,
        city=addr.city,
        state=addr.state,
        zip_code=addr.zipcode
    )
    return json.loads(json.dumps(v))


def get_cached_verification(addr: ParsedAddress) -> Verification:
    global _vmap

    if _vmap is None:
        _vmap = load_from_cache()
    if addr not in _vmap:
        _vmap[addr] = get_verification(addr)
        save_to_cache(_vmap)
    return _vmap[addr]


def load_from_cache() -> VerificationMap:
    if not CACHE_PATH.exists():
        save_to_cache({})
    return pickle.loads(CACHE_PATH.read_bytes())


def save_to_cache(vmap: VerificationMap):
    CACHE_PATH.write_bytes(pickle.dumps(vmap))


if __name__ == '__main__':
    stats = {
        'total': 0,
        'incomplete': 0
    }
    exit_code = 0
    for addr in parse_landlord_addresses():
        stats['total'] += 1
        print(
            repr(addr.raw_address),
            '(looked up in NYCDB)' if addr.is_looked_up else '(manually entered)'
        )
        parsed = addr.parsed_address
        print(f"  parsed: {parsed.short_desc()}")
        if parsed.is_populated():
            try:
                ver = get_cached_verification(parsed)
            except lob.error.APIError as e:
                # This is likely something along the lines of
                # "You have exceeded the 300 free US Verifications limit", but
                # regardless, just stop and print stats.
                print(e)
                exit_code = 1
                break
            deliverability = ver['deliverability']
            if deliverability not in stats:
                stats[deliverability] = 0
            stats[deliverability] += 1
            print(f"  deliverability: {deliverability}")
        else:
            stats['incomplete'] += 1
            print(f"  incomplete address (undeliverable)")
    for key in stats:
        print(f"{key} addresses: {stats[key]}")
    sys.exit(exit_code)
