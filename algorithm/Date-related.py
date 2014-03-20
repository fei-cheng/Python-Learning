from datetime import date

dt = date(2012,12,22)  #new world

"""
    read-only
"""
year  = dt.year
month = dt.month
day   = dt.day

day_of_week = dt.weekday() #Sunday as 1
iso_day_of_week = dt.isoweekday()  #Begin with Monday
dt_fmt = dt.isoformat()

today = date.today()


"""
    class attributes
"""
max_dt = date.max
min_dt = date.min
res_dt = date.resolution  #timedelta(days=1)
