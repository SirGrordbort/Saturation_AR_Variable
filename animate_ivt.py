import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
    # ------------

fig = plt.figure()
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
line, = ax.plot([], [], lw=2)


# initialization function
def init():
    # creating an empty plot/frame
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent((-90, 30, -70, 0), crs=ccrs.PlateCarree(central_longitude=180))
    ax.outline_patch.set_visible(False)
    # Add coastlines
    ax.coastlines(resolution='50m', color='black', linewidth=0.5)


# lists to store x and y axis points
xdata, ydata = [], []


# animation function
def animate(i):
    # t is a parameter
    t = 0.1 * i

    # x, y values to be plotted
    x = t * np.sin(t)
    y = t * np.cos(t)

    # appending new points to x, y axes points list
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)
    return line,


# setting a title for the plot
plt.title('Creating a growing coil with matplotlib!')
# hiding the axis details 
plt.axis('off')

# call the animator	 
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=20, blit=True)

# save the animation as mp4 video file 
anim.save('coil.gif', writer='imagemagick')