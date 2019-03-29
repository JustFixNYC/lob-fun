This is an experiment in using [usaddress][] to parse landlord
addresses and [Lob][] to verify them.

## Quick start

First dump `LandlordDetails` models from the [tenants2][] app:

```
python manage.py dumpdata loc.LandlordDetails > /path/to/lob-fun-repo/landlords.json
```

Then create your `.env` file:

```
cp .env.sample .env
```

Now edit `.env` as needed.

Then setup and enter a virtualenv from the root of the repo:

```
python3 -m venv venv
source venv/bin/activate  # Or 'venv/Scripts/activate' on Windows
pip install -r requirements.txt
```

To parse and verify addresses:

```
python verifyaddrs.py
```

## Running tests

```
mypy . && pytest
```

[usaddress]: https://github.com/datamade/usaddress
[Lob]: https://lob.com
[tenants2]: https://github.com/justFixNYC/tenants2
