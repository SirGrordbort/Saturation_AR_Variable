
# get_max_sat_cube
A program for calculating NIVT from variables downloaded from the copernicus database.
This is the program discussed in the report

# time_max_sat
Same asget_max_sat_cube but can iterate over multiple time steps

# arc_average_tool
A tool for ArcGis to find ars based on fraction of full saturation combined with wind speed.
Also contains some utility scripts for this process.

# animate_ivt
A work in progress for animating plots of IVT, IWV and NIVT over time

# create_station_points
Uses ArcGIS to plot the locations of NZ whether stations on a map


# get_max_saturation
Similar in functionality to get_max_sat_cube but uses the arcpy library in stead of iris cube 
and so is significantly slower

# get_saturation
Plots the results of get_max_saturation on an ArcGIS map

# plot_rainfall
An early work in progress to plot NIVT against rainfall

# real_max_sat
An alternate version of get_max saturation so I don't break it when testing

# split_coord_column
A utility script for create_station_points

