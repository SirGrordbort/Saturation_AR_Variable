
import arcpy

"""
A script for splitting the station identifier text given by cliflo
as a single text column with the latitude and longitude, into two
new latitude and longitude columns of type float. It then creates
a point feature class based on the new table.
"""

def split_coord_column():

    cliflo_table = arcpy.GetParameter(0)
    point_class = arcpy.GetParameter(1)

    arcpy.AddField_management(cliflo_table, "lat", "DOUBLE")
    arcpy.AddField_management(cliflo_table, "lon", "DOUBLE")

    table_cursor = arcpy.da.UpdateCursor(cliflo_table, ("Station", "lat", "lon"))
    for row in table_cursor:
        lat_lon = row[0]
        lat, lon = split_in_two(lat_lon)
        row[1] = lat
        row[2] = lon
        table_cursor.updateRow(row)

        # create output
        arcpy.XYTableToPoint_management(cliflo_table, point_class, "lon", "lat")





def split_in_two(lat_lon_str):
    """
    A function for splitting a string of lat-long to two separate float
    values for that lat-long.
    :param lat_lon_str: (string)a comma separated string containing the
    latitude and longitude
    :return lat: (float) the latitude from the given string converted to
    a float and rounded to 4dp
    :return lon: (float) the longitude from the given string converted to
    a float and rounded to 4dp
    """
    assert isinstance(lat_lon_str, str), "not a string"
    lat_lon_split = lat_lon_str.split(",")
    arcpy.AddMessage(lat_lon_split)
    arcpy.AddMessage(lat_lon_split[0])
    arcpy.AddMessage(float(lat_lon_split[0]))
    arcpy.AddMessage(round(float(lat_lon_split[0]), 4))

    lat = round(float(lat_lon_split[0]), 4)
    lon = round(float(lat_lon_split[1]), 4)
    return lat, lon


split_coord_column()
