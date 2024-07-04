import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from osgeo import gdal
import numpy as np

def read_raster(file_path):
    dataset = gdal.Open(file_path)
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()
    no_data_value = band.GetNoDataValue()
    data[data == no_data_value] = np.nan  
    transform = dataset.GetGeoTransform()
    return data, transform

def plot_raster(ax, m, data, transform, cmap, title):
    nrows, ncols = data.shape
    x0, dx, _, y0, _, dy = transform
    x = np.linspace(x0, x0 + dx * ncols, ncols)
    y = np.linspace(y0, y0 + dy * nrows, nrows)
    x, y = np.meshgrid(x, y)
    im = m.pcolormesh(x, y, data, cmap=cmap, shading='auto', latlon=True)
    ax.set_title(title)
    return im

def main():
    raster1_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\Slope1.tif'
    raster2_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\Slope2.tif'

    data1, transform1 = read_raster(raster1_path)
    data2, transform2 = read_raster(raster2_path)

    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    m1 = Basemap(projection='cyl', llcrnrlat=31.23, urcrnrlat=32.62,
                 llcrnrlon=118.353048, urcrnrlon=119.243048, resolution='i', ax=ax[0])
    m1.drawcoastlines()
    m1.drawcountries()
    m1.drawparallels(np.arange(31.23, 32.62, 0.2), labels=[1, 0, 0, 0])
    m1.drawmeridians(np.arange(118.353048, 119.243048, 0.2), labels=[0, 0, 0, 1])
    im1 = plot_raster(ax[0], m1, data1, transform1, plt.cm.viridis, "Nanjing Pvalue")

    m2 = Basemap(projection='cyl', llcrnrlat=31.23, urcrnrlat=32.62,
                 llcrnrlon=118.353048, urcrnrlon=119.243048, resolution='i', ax=ax[1])
    m2.drawcoastlines()
    m2.drawcountries()
    m2.drawparallels(np.arange(31.23, 32.62, 0.2), labels=[1, 0, 0, 0])
    m2.drawmeridians(np.arange(118.353048, 119.243048, 0.2), labels=[0, 0, 0, 1])
    im2 = plot_raster(ax[1], m2, data2, transform2, plt.cm.inferno, "Nanjing Slope")

    fig.colorbar(im1, ax=ax[0], orientation='horizontal', fraction=0.05, pad=0.05)
    fig.colorbar(im2, ax=ax[1], orientation='horizontal', fraction=0.05, pad=0.05)

    plt.show()

if __name__ == "__main__":
    main()
