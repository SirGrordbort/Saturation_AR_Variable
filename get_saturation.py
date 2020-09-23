import arcpy
import math

def make_points(lon, lat, length, width):
    points = arcpy.Array()
    points.append(arcpy.Point(lat, lon))
    points.append(arcpy.Point(lat+width, lon))
    points.append(arcpy.Point(lat + width, lon + length))
    points.append(arcpy.Point(lat, lon+length))
    points.append(points[0])
    return points

table = arcpy.GetParameter(0)
out_feature = arcpy.GetParameter(1)
table_cursor = arcpy.da.SearchCursor(table, ("latitude", "longitude", "time", "IVT_N", "IVT_E", "max_q"))
add_polys = arcpy.da.InsertCursor(out_feature, ("time", "Shape@", "NORMIVT"))
count = 0
for lat_lon in table_cursor:
    lat = lat_lon[0]
    lon = lat_lon[1]
    points = make_points(lat, lon, 0.25, 0.25)
    arcpy.AddMessage(str(points))
    poly = arcpy.Polygon(points)
    tot_IVT = math.hypot(lat_lon[3], lat_lon[4])
    normIVT = float(tot_IVT)/float(lat_lon[5])
    add_polys.insertRow((lat_lon[2], poly, normIVT))

