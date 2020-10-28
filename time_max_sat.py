# ------------------- Import Modules and Packages --------------------
# --------------------------------------------------------------------
# Import Modules and Packages
import cartopy.crs as ccrs
from cf_units import Unit
import iris
import iris.quickplot as qplt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
import math

# ------------------------------ Plot --------------------------------
# Add a matplotlib Axes, specifying the display projection
def plot_cube(variable_cube, f_name, title, variable):
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude=180))
    ax.set_extent((-90, 30, -70, 0), crs = ccrs.PlateCarree(central_longitude=180))
    ax.outline_patch.set_visible(False)
    # Add coastlines
    ax.coastlines(resolution='50m', color='black', linewidth=0.5)
    # Plot Contour
    contour = (iris.plot.contourf(variable_cube, cmap=matplotlib.cm.get_cmap('Blues')))
    # Plot Colorbar
    cbar = plt.colorbar(contour, shrink = 0.55)
    cbar.set_label(variable, rotation=270, labelpad = 10, fontsize=8)
    # Plot Title
    plt.title(title, fontdict = {'fontsize' : 10})
    # Save Figure
    plt.savefig(f_name + '.png', dpi=700)
    plt.close()
    # ---------------------------------------------------------------------


num_steps = 1
cubes = []  # list of cubes, one for each time step
# download_data
for step in range(num_steps):
    #load data
    iwv = iris.load('single_lvl_data.nc', 'tcwv')[0][step] # IWV
    u_ivt = iris.load('single_lvl_data.nc', 'p71.162')[0][step] # Eastward IVT
    v_ivt = iris.load('single_lvl_data.nc', 'p72.162')[0][step] # Northward IVT
    tp = iris.load('single_lvl_data.nc', 'tp')[0][step] # Total precipitation
    sp = iris.load('single_lvl_data.nc', 'sp')[0][step] # Surface pressure
    sp.convert_units('hPa') # Convert to hPa
    t2m = iris.load('single_lvl_data.nc', 't2m')[0][step] # 2m temperature
    t2m.convert_units('Celsius')
    d2m = iris.load('single_lvl_data.nc', 'd2m')[0][step] # 2m dewpoint temperature
    d2m.convert_units('Celsius')
    u10 = iris.load('single_lvl_data.nc', 'u10')[0][step] # 10m u wind
    v10 = iris.load('single_lvl_data.nc', 'v10')[0][step] # 10m v wind
    # Pressure Level Data
    t = iris.load('p_lvl_data.nc', 't')[0][step] # Temperature
    t.convert_units('Celsius')
    u = iris.load('p_lvl_data.nc', 'u')[0][step] # u wind
    v = iris.load('p_lvl_data.nc', 'v')[0][step] # v wind
    q = iris.load('p_lvl_data.nc', 'q')[0][step] # Specific humidity
    # --------------------------------------------------------------------

    # --------------------- Define Other Variables -----------------------
    pressure_levels = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750,
                       800, 850, 900, 925, 950, 975, 1000]
    g = 9.807 # Gravity
    e0 = 6.11 # Saturation vapour pressure at T0 in hPa
    eps = 0.622 # Ratio of Rd/Rv in kg/kg
    # --------------------------------------------------------------------

    # ------------------- Calculate Derived Variables --------------------
    # Create cube with all entries zero
    s_zero = (t2m.copy() * 0) # Same dimensions as single level data
    p_zero = (t.copy() * 0) # Same dimensions as pressure level data
    s_zero.units = Unit('Unknown') # Erase units
    p_zero.units = Unit('Unknown') # Erase units
    # Calculate variables
    e_sfc = s_zero.copy()
    q_sfc = s_zero.copy()
    e_sfc.data = e0 * np.exp((17.27 * d2m.data)/(d2m.data + 237.3))
    q_sfc.data = (eps * e_sfc.data)/(sp.data - ((1-eps) * e_sfc.data))
    # --------------------------------------------------------------------

    p = p_zero
    for i in range(17):
        p.data[i] = pressure_levels[i]

    # ------------------------ Calculate Variable ------------------------
    # Calculate integrand for max saturation on pressure levels
    integrand_p = p_zero.copy()
    integrand_p.data = 0.622 * (0.611 * np.exp((17.27 * t.data)/(t.data + 237.3))) / (g * p.data/10) # divide by 10 to convert hectopascals to kilopascals
    # Calculate integrand at surface
    integrand_sfc = s_zero.copy()
    integrand_sfc.data = 0.622 * (0.611 * np.exp((17.27 * t2m.data)/(t2m.data + 237.3))) / (g * sp.data/10)

    # Append surface integrand to pressure level integrand
    integrand = np.concatenate((integrand_p.data, [integrand_sfc.data]))
    # Create pressure level array
    p = p_zero.copy()
    for i in range(len(pressure_levels)):
        p.data[i] = pressure_levels[i]
    # Append surface pressure to pressure level array
    p_array = np.concatenate((p.data, [sp.data]))
    # Sort integrand and pressure level array
    p_inds = np.argsort(p_array, axis = 0)
    sorted_p_array = np.take_along_axis(p_array, p_inds, axis=0)
    sorted_integrand_array = np.take_along_axis(integrand, p_inds, axis=0)
    # We integrate from surface to min pressure. Therefore replace all
    # pressure values > surface pressure (i.e below the surface) with
    # surface pressure.
    sorted_p_array = np.fmin(sorted_p_array, sp.data)
    # Numerically integrate (trapezoidal rule)
    integral = scipy.integrate.trapz(sorted_integrand_array,
                                     sorted_p_array * 100,
                                     axis = 0)
    # Set Variable Cube
    variable_cube = s_zero.copy()
    variable_cube.data = integral.data

    # plot_cube(variable_cube, "max_sat", "max column water", "water vapour (kg/m squared")
    # plot_cube(iwv, "iwv", "actual column water", "water vapour (kg/m squared)")
    # --------------------------------------------------------------------

    # make max saturation variable
    norm_ivt = s_zero.copy()
    norm_ivt.data = u_ivt.data**2+v_ivt.data**2
    norm_ivt.data = norm_ivt.data**0.5
    norm_ivt.data = norm_ivt.data/variable_cube.data
    cubes.append(norm_ivt)
    plot_cube(norm_ivt, "norm_ivt "+str(step), "normalised ivt", "normalised ivt (kg/ms)")
    print("loop num " + str(step))
cube_list = iris.cube.CubeList(cubes)
time_cube = cube_list.merge()
iris.save(time_cube[0],"mycube.nc")
print("done")