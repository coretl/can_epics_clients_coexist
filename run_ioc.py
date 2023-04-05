from pathlib import Path
from epicscorelibs.ioc import start_ioc
import time
here = Path(__file__).absolute().parent
start_ioc(str(here/"record.db"))
time.sleep(60)
