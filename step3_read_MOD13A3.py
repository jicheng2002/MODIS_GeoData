import os,glob
import re
import time
import shutil
import numpy as np
import multiprocessing 
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly

# set workspace
s = os.sep
# the layers to be extracted
layers = ["NDVI","EVI"]

pathrd = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\MOD13A3'
pathwt =r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Tif'

def HDF2Geotiff(input_file): 
    try:
        dataSource = gdal.Open(input_file)
        # get the data list inside the HDF4 file
        subDatasets = dataSource.GetSubDatasets()
        print(subDatasets)
        for i, layer in enumerate(layers):
            i= 0
            print(i)
            print(layer)
            layer = layers[0]
            # select band
            subData_ = [x[0] for x in subDatasets if re.match(''.join(['.*:1 km monthly ',layers[i],"$"]), x[0], re.IGNORECASE)] 
            subData = gdal.Open(subData_[0], GA_ReadOnly)
            nodata = subData.GetRasterBand(1).GetNoDataValue() 
            datatype = subData.GetRasterBand(1).DataType

            # (x_top_left, x_resolution, rotation, y_top_left, rot
            geotransform = subData.GetGeoTransform()
            projection = subData.GetProjection()
            # ncols
            xsize = subData.RasterXSize
            # nrows
            ysize = subData.RasterYSize
            # get the array
            array = subData.ReadAsArray()
            # get the year of the file
            filename = os.path.basename(input_file)

            #保存数据
            newfile = pathwt   + s + filename + "_" + layers[i] + '.tif'
            driver = gdal.GetDriverByName('GTiff')
            # if file exist, remove it
            if os.path.exists(newfile):
                os.remove(newfile)
            # create single band geotiff
            target = driver.Create(newfile, xsize, ysize, 1, datatype, ['COMPRESS=LZW'])
            target.SetGeoTransform(geotransform)
            target.SetProjection(projection)
            target.GetRasterBand(1).WriteArray(array)
                # set No data
            target.GetRasterBand(1).SetNoDataValue(nodata)
            target.FlushCache()
    except Exception as e:
        pass

if __name__ == "__main__":
    # start time
    start_time = time.time()
    hdffiles = []
    for root, dirs, files in os.walk(pathrd):
        print(root)
        print('------')
        print(dirs)
        print('****')
        print(files)

        if (len(files)>0):
            [hdffiles.append(root+'\\'+file) for file in files]

    hdffiles = sorted(hdffiles)
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores-2)
    pool.map(HDF2Geotiff, hdffiles)
    pool.close()
    pool.join()

    # end time
    print("running time: %s" % (time.time() - start_time))



