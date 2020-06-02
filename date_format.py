import os
import sys
import time
from datetime import date
from datetime import timedelta


today = date.today()
start_date = date(today.year, 6, 1)
end_date = date(today.year, 9, 30)

date_len = 1000

date_list = []

def populate_date():
    cur_date = start_date
    for i in range(1,date_len):
        date_list.append(str(cur_date))
        d = timedelta(days=1)
        cur_date = cur_date + d
        if cur_date > end_date:
            break
            #print (cur_date)


populate_date()


print (date_list)

