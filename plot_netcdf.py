from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

"""
Define here the data file (ifile), the name of the variable in the file (ifile) and the latitutde you want to interpolate (interpolated_lat).

If you don't know the variable name as it is in the file, run:
ncdump -h <ifile>
outside of this script, in the terminal.

If everything runs good, you should see the new file figure.png in the folder where is this script.
"""

ifile = '/chemie/pavlea/p100m0-gm/echam5/p100m0-gm_CHEM_6h_207604.nc'
varname = 'TOTOZ'
interpolated_lat = 1.8

# reading netcdf file. I assume var is in time x lat x lon
with Dataset(ifile) as nc:
    time = nc.variables['time'][:]
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    var = nc.variables[varname][:]

"""
Making the zonal mean of the variable - averaging over 3rd dimension (lon)
0 is the first dimension in Python by definition
"""
var_zm = np.mean(var, axis=2)

# making the interpolation function f
f = interpolate.interp1d(lat, var_zm)
# applying the function of the lat you want to interpolate
var = f(interpolated_lat)

# defining the size of the graph (9,5) (length,height)
fig = plt.figure(figsize=(9, 5))
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

""" 
plotting the graph.
x-axis is time
y-axis is variable
"k" is black color
linewidth is the width of the graph
"""

plt.plot(time, var, color = "k", linewidth = 3)

# disable minor ticks - ticks between the 'major' ticks.
axes.minorticks_off()

# length, width of major ticks
axes.tick_params('both', length=5, width=1, which='major',direction='out')

# we have ticks only on the left side and at the bottom of the graph
axes.yaxis.set_ticks_position('left')
axes.xaxis.set_ticks_position('bottom')

# setting the font size (10) of x and y labels
for item in (axes.get_xticklabels() + axes.get_yticklabels()):
        item.set_fontsize(10)

# labeling y and x axis as time (x) and name of the variable (y)
axes.set_ylabel(varname,fontsize=10)
axes.set_xlabel('time',fontsize=10)

# removing top and right line of the graph
axes.spines['top'].set_visible(False)
axes.spines['right'].set_visible(False)

# title of the graph
plt.title(varname+' at '+str(interpolated_lat)+'°', fontsize=12)

# ranges of the graph (x-start, x-end, y-start, y-end)
plt.axis([time.min() , time.max() , var.min(), var.max()])

# saving a graph as figure.png in the same folder where is this script
fig.savefig('figure.png',bbox_inches='tight')
# closing
plt.close(fig)
