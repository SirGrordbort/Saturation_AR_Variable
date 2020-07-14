import split_coord_column
import arcpy
"""
Creates a point feature class using the coordinates of the given stations and
associated data (e.g. rainfall at those stations). The coordinates of the
stations are split from one into two columns before the point class can be 
created.
"""
def create_station_points():
    cliflo_table = arcpy.GetParameter(0)  # input table
    point_class = arcpy.GetParameter(1)  # output point feature class

    station_table = split_coord_column.split_coord_column(cliflo_table)
    arcpy.XYTableToPoint_management(station_table, point_class, "lon", "lat")


if __name__ == '__main__':
    create_station_points()
