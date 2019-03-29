## Quick start

First dump `LandlordDetails` models from the [tenants2][] app:

```
python manage.py dumpdata loc.LandlordDetails > /path/to/lob-fun-repo/landlords.json
```

Then setup and enter a virtualenv from the root of the repo:

```
python3 -m venv venv
source venv/bin/activate  # Or 'venv/Scripts/activate' on Windows
```

To parse addresses:

```
python parseaddrs.py
```

## Running tests

```
mypy . && pytest
```

[tenants2]: https://github.com/justFixNYC/tenants2
