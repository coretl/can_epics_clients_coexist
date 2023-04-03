# can_epics_clients_coexist
Tests to see if we can make various CA and PVA clients coexist

# Install

Make a venv and install requirements:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install epicscorelibs pyepics aioca pvapy p4p
```

# Run the ioc
```bash
python -m epicscorelibs.ioc -d record.db
```

# Run the tests
Uncomment *one* of the tests in the `__main__` section of `test_clients.py`, then:
```bash
python test_clients.py
```

# Get the backtrace
If looking at a failing test can get backtrace under gdb:
```bash
gdb python
run test_clients.py
```