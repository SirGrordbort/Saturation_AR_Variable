import arcpy
import datetime
import numpy as np
import scipy.integrate as integrate
import math

def make_where(latitude, longitude, date):
    where_string = "latitude = %d, longitude = %d, "%(latitude, longitude)
    date_string = "date = " + str(date)
    return where_string+date_string


def make_dates(num_steps):
    start = datetime.datetime(2018, 10, 1, 0)
    date_list = [start - datetime.timedelta(hours=6*x) for x in range(num_steps)]
    return date_list


def calc_max_q(temp):
    return 0.611*math.exp((17.27*temp)/(temp+237.3))

temp_table = arcpy.GetParameter(0)
out_table = arcpy.GetParameter(1)
dates = make_dates(11)
new_rows = arcpy.da.InsertCursor(out_table, ("latitude", "longitude", "date", "max_q"))

arcpy.AddMessage("loaded tables and dates")
for lat in np.arange(-70.0, 0, 0.25):
    for lon in np.arange(90, 210, 0.25):
        for date in dates:
            where = make_where(lat, lon, date)
            pressure_levels = arcpy.da.SearchCursor(temp_table, ("temperature", "pressure"), where_clause=where)
            pressure = []  # assume sorted for now
            max_q = []
            for row in pressure_levels:
                max_q.append(calc_max_q(row[0]))
                pressure.append(row[1])
            integrated_max_q = integrate.trapz(max_q, pressure * 100, axis=0)
            new_rows.insert(lat, lon, date, integrated_max_q)
arcpy.AddMessage("completed")


