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

import pymongo
password = os.environ["GSHEETS"]
mongo_uri = "mongodb://johncoogan:%s@lighthouse.1.mongolayer.com:10243,lighthouse.0.mongolayer.com:10243/testing" % password
connect = pymongo.Connection(mongo_uri)
mongo = connect.sleeplog



# target = sheetsync.Sheet(username=username, password=password, document_name="SleepLog")

results = {'datetime': local_date, 'datestr': local_str, 'force': float(sys.argv[1]), 'bumps': int(sys.argv[2])}

# target.inject({local_str:results})

mongo.save(results)