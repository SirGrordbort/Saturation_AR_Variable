import arcpy
import make_point as mkpt
import math
table = arcpy.GetParameter(0)
out_feature = arcpy.GetParameter(1)
table_cursor = arcpy.da.SearchCursor(table, ("latitude", "longitude", "time", "IVT_N", "IVT_E", "qmax"))  # FIXME IVT needs to be calculated first
add_polys = arcpy.da.InsertCursor(out_feature, ("time", "poly", "NORMIVT"))
for lat_lon in table_cursor:
    lat = lat_lon[0]
    lon = lat_lon[1]
    points = mkpt.make_points(lat, lon, 0.25, 0.25)
    poly = arcpy.Polygon(points)
    tot_IVT = math.hypot(lat_lon[4], lat_lon[5])
    normIVT = tot_IVT/lat_lon[6]
    add_polys.insertRow(lat_lon[3], poly, normIVT)

