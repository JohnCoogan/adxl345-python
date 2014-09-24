import os
import sys
from datetime import datetime
from pytz import timezone
import pytz
import pymongo

def post_results():
    date_format='%Y-%m-%d %H:%M:%S'
    utc_date = datetime.now(tz=pytz.utc)
    local_date = utc_date.astimezone(timezone('US/Pacific'))
    local_str = local_date.strftime(date_format)


    password = os.environ["MONGOPW"]
    mongo_uri = "mongodb://johncoogan:%s@lighthouse.1.mongolayer.com:10243,lighthouse.0.mongolayer.com:10243/testing" % password
    connect = pymongo.Connection(mongo_uri)
    mongo = connect.testing
    sleeplog = mongo.sleeplog

    results = {'datetime': local_date, 'datestr': local_str, 'force': float(sys.argv[1]), 'bumps': int(sys.argv[2]), 'bumpforce': float(sys.argv[3])}

    sleeplog.save(results)
    return True



if __name__ == '__main__':
    post_results()
    sys.exit(1)
