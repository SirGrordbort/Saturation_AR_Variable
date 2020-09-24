import arcpy
import datetime
import numpy as np
import scipy.integrate as integrate
import math


def make_where(latitude, longitude, date):
    """Makes an SQL query for finding all rows with a given latitude, longitude and time.
    In this case the query will find all pressure level entries for the fields specified above"""

    where_string = "latitude = %f AND longitude = %f AND " % (latitude, longitude)
    date_string = "time = date '" + str(date) + "'"
    return where_string + date_string


def make_dates(num_steps):
    """Makes a list of times starting from 3/10/2018 at 6pm and including all dates at 6hr times steps up to the number
     specified in the parameter num_steps """

    start = datetime.datetime(2018, 10, 3, 18)
    date_list = [start - datetime.timedelta(hours=6 * x) for x in range(num_steps)]
    return date_list


def calc_max_q(temp):
    """calculate maximum saturation based on temperature using Tetens equation"""
    return 0.611 * math.exp((17.27 * temp) / (temp + 237.3))


try:

    # gets tool input parameters from ArcGIS
    temp_table = arcpy.GetParameter(0)
    mid_table = arcpy.GetParameter(1)

    # list of dates to be iterated over
    dates = make_dates(11)

    # Cursor for inserting calculated values into the output
    new_rows = arcpy.da.InsertCursor(mid_table, ("latitude", "longitude", "time", "max_q"))

    # range of lat and lon specified in the data
    lats = np.arange(-70.0, 0, 0.25)
    longs = np.arange(90, 210, 0.25)

    for lat in lats:
        for lon in longs:
            for date in dates:

                # returns all temperatures and pressure levels for a given coordinate and date
                where = make_where(lat, lon, date)
                pressure_levels = arcpy.da.SearchCursor(temp_table, ("t", "level"), where_clause=where)
                arcpy.AddMessage(where)

                pressure = []  # assumes pressures are added smallest to largest (which they are so far)
                max_q = []
                for row in pressure_levels:
                    max_q.append(calc_max_q(row[0]))
                    pressure.append(row[1])
                del pressure_levels

                # skips computation if there is none to do
                if len(pressure) == 0 or len(max_q) == 0:
                    continue

                # gets integrated max_q and adds it to the output
                integrated_max_q = integrate.trapz(max_q, pressure, axis=0)  # TODO had pressure times 1000 find out why
                new_rows.insertRow((lat, lon, date, integrated_max_q))
    arcpy.AddMessage("completed")

finally:
    # ensures the insert cursor is deleted no matter when the program stops so that it doesn't cause a memory leak. not
    # 100% sure this is necessary but easy to do just in case
    del new_rows
