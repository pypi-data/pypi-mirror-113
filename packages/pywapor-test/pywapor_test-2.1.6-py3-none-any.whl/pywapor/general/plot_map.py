import gdal
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_tif(tif_file, quantity = None, unit = None):
    ds = gdal.Open(tif_file)
    array = ds.GetRasterBand(1).ReadAsArray()
    ndv = ds.GetRasterBand(1).GetNoDataValue()

    array[array == ndv] = np.nan

    mini = np.nanpercentile(array, 5)
    maxi = np.nanpercentile(array, 95)

    fn = os.path.split(tif_file)[-1]

    plt.imshow(array, vmin = mini, vmax = maxi)
    plt.colorbar(label = f"{quantity} {unit}", extend = "both")
    plt.title(fn)
    plt.gca().set_facecolor("lightgray")

# tif_file = r"/Users/hmcoerver/Downloads/normal_MODIS/RAW/LST/MOD11/Daily/LST_MOD11A1_K_daily_2019.07.06.1025.tif"
# quantity = "LST"
# unit = "[K]"

# plot_tif(tif_file, quantity = quantity, unit = unit)