import arcpy
import datetime
import numpy as np
import scipy.integrate as integrate
import math

def make_where(latitude, longitude, date):
    where_string = "latitude = %f AND longitude = %f AND " % (latitude, longitude)
    date_string = "time = date '" + str(date)+"'"
    return where_string+date_string


def make_dates(num_steps):
    start = datetime.datetime(2018, 10, 4, 0)
    date_list = [start - datetime.timedelta(hours=6*x) for x in range(num_steps)]
    return date_list


def calc_max_q(temp):
    return 0.611*math.exp((17.27*temp)/(temp+237.3))


try:

    temp_table = arcpy.GetParameter(0)
    mid_table = arcpy.GetParameter(1)
    dates = [datetime.datetime(2018, 10, 4, 6), datetime.datetime(2018, 10, 3, 6)]  # make_dates(11) TODO reinstate after testing
    new_rows = arcpy.da.InsertCursor(mid_table, ("latitude", "longitude", "time", "t"))

    lats = [-70,-60,-50]# np.arange(-70.0, 0, 0.25) FIXME reinsert this code after testing
    longs = [90,95,110]# np.arange(90, 210, 0.25)
    for lat in lats:
        for lon in longs:  # FIXME these are iterating with whole numbers still
            for date in dates:
                where = make_where(lat, lon, date)
                arcpy.AddMessage(where)
                pressure_levels = arcpy.da.SearchCursor(temp_table, ("t", "level"), where_clause=where)
                pressure = []  # assume sorted for now
                max_q = []
                for row in pressure_levels:
                    arcpy.AddMessage("iterated")
                    max_q.append(calc_max_q(row[0]))
                    pressure.append(row[1])

                del pressure_levels
                arcpy.AddMessage("pressures " + str(pressure))
                arcpy.AddMessage("max_qs " + str(max_q))
                if len(pressure) == 0 or len(max_q) == 0:
                    continue
                integrated_max_q = integrate.trapz(max_q, pressure, axis=0) # TODO had pressure times 1000 find out why
                new_rows.insertRow((lat, lon, date, integrated_max_q))
    arcpy.AddMessage("completed")

finally:
    del new_rows


