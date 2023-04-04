# can_epics_clients_coexist
Tests to see if we can make various CA and PVA clients coexist

# Install

Make a venv and install requirements:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install epicscorelibs pyepics aioca pvapy p4p
```

# Run the tests
Run a combination of:
- aioca - CA using epicscorelibs
- p4p - PVA using epicscorelibs
- pvapy - PVA bundled
- pyepics - CA bundled
- epicscorelibs - to make pyepics use epicscorelibs instead of bundled libs

Pass them in order to the test script, it will run up an IOC then do the imports in that order and do 5 gets in turn from each client
```bash
python test_clients.py aioca p4p pvapy
```

# Get the backtrace
If looking at a failing test can get backtrace under gdb:
```bash
gdb python
run test_clients.py aioca p4p pvapy
```