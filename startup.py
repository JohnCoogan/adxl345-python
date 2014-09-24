import os
import sys
from datetime import datetime
from pytz import timezone
import pytz
import pymongo

def post_status():
    date_format='%Y-%m-%d %H:%M:%S'
    utc_date = datetime.now(tz=pytz.utc)
    local_date = utc_date.astimezone(timezone('US/Pacific'))
    local_str = local_date.strftime(date_format)


    password = os.environ["MONGOPW"]
    mongo_uri = "mongodb://johncoogan:%s@lighthouse.1.mongolayer.com:10243,lighthouse.0.mongolayer.com:10243/testing" % password
    connect = pymongo.Connection(mongo_uri)
    mongo = connect.testing
    statuslogs = mongo.statuslogs

    current_status = {'datetime': local_date, 'datestr': local_str, 'status': 'alive'}

    statuslogs.save(current_status)
    return True


if __name__ == '__main__':
    post_status()
    sys.exit(1)
