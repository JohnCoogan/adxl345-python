import os
import sys
import sheetsync
from datetime import datetime
from pytz import timezone
import pytz

date_format='%Y-%m-%d %H:%M:%S'
utc_date = datetime.now(tz=pytz.utc)
local_date = utc_date.astimezone(timezone('US/Pacific'))
local_str = local_date.strftime(date_format)

password = os.environ["GSHEETS"]
username = "coogan.johna@gmail.com"

target = sheetsync.Sheet(username=username, password=password, document_name="SleepLog")

results = {'force': float(sys.argv[1]), 'bumps': int(sys.argv[2])}

target.inject({local_str:results})
