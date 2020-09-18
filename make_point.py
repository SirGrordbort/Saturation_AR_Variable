import arcpy


def make_points(lat, lon, length, width):
    points = []
    points.append(arcpy.Point(lat, lon))
    points.append(arcpy.Point(lat+width, lon))
    points.append(arcpy.Point(lat, lon+length))
    points.append(arcpy.Point(lat + width, lon + length))
    points.append(points[0])
    return points

