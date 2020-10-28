import arcpy
import math

def make_points(lon, lat, length, width):
    """Creates an arcpy array of points which become the vertices for a new polygon"""
    w = width/2.0
    l = length/2.0
    points = arcpy.Array()
    points.append(arcpy.Point(lat+w, lon+l))
    points.append(arcpy.Point(lat+w, lon-l))
    points.append(arcpy.Point(lat-w, lon-l))
    points.append(arcpy.Point(lat-w, lon+l))
    points.append(points[0])
    return points

# gets inputs from ArcGis tool
table = arcpy.GetParameter(0)
out_feature = arcpy.GetParameter(1)

# For each row in the input table a polygon is made from the coordinates which contains the normalised IVT and time.
table_cursor = arcpy.da.SearchCursor(table, ("latitude", "longitude", "time", "NORMIVT"))
add_polys = arcpy.da.InsertCursor(out_feature, ("time", "Shape@", "NORMIVT"))
for lat_lon in table_cursor:
    lat = lat_lon[0]
    lon = lat_lon[1]
    points = make_points(lat, lon, 0.25, 0.25)
    poly = arcpy.Polygon(points)
    add_polys.insertRow((lat_lon[2], poly, lat_lon[3]))

