# import glob,os
# import numpy as np
# from osgeo import gdal
# from scipy.stats import linregress
# import time

# start_time = time.time()
# MOD13A3Crop = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Wrap"
# tiffiles = glob.glob(MOD13A3Crop + '/'+ '*.tif')
# tiffiles = sorted(tiffiles)
# years = np.arange(2015,2020)

# #fliter files in July
# month = '07'
# spectifs = []
# for tiffile in tiffiles:
#     #print(tiffile)
#     #tiffile = tiffiles[0]
#     monthstr = tiffile.split('.')[-3][-2:] 
#     if monthstr == month:
#         spectifs.append(tiffile)
        
# #read flitered files and put them into 3-d array
# images_list = [] 
# for spectif in  spectifs:       
#     raster = gdal.Open(spectif)
#     geotransform = raster.GetGeoTransform()
#     projection = raster.GetProjection()
#     band = raster.GetRasterBand(1)
#     image_array = band.ReadAsArray()
#     images_list.append(image_array)

# images_array_3d = np.array(images_list)/1.0
# images_array_3d[images_array_3d<=-3000] = np.nan
# images_array_3d[images_array_3d>=10000] = np.nan
# images_array_3d = images_array_3d/10000.0
# #np.where(np.logical_and(images_array_3d[0,:,:]==0.745,images_array_3d[1,:,:]==0.6952))


# num_rows, num_cols = images_array_3d[0].shape
# slope_array = np.zeros((num_rows, num_cols))
# slope_array[slope_array==0] = np.nan

# p_array = np.zeros((num_rows, num_cols))
# p_array[p_array==0] = np.nan

# years = years.reshape(-1, 1)
# #conduct on each pixel
# for i in range(num_rows):
#     print(i)
#     for j in range(num_cols):
        
#         pixel_data = images_array_3d[:, i, j]
#         nansize = np.size(np.where(np.isnan(pixel_data)))
        
#         if nansize>=0 and nansize<=3:
#             validIndex = np.where(~np.isnan(pixel_data))
#             year_array1 = np.squeeze(years[validIndex])
#             pixel_data1 = pixel_data[validIndex]
            
            
#             # linear regression
#             slope, intercept, r_value, p_value, std_err = linregress(year_array1, pixel_data1)
#             slope_array[i, j] = slope
#             p_array[i, j] = p_value  
 
           
# slope_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\MODD13A3.007.Slope.tif'
# p_path = r'D:D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\MODD13A3.007.Pvalue.tif'
# save_path = [slope_path,p_path]
# save_array = [slope_array, p_array]

# for n in [0,1]:
#     driver = gdal.GetDriverByName('GTiff')
#     raster = driver.Create(save_path[n], num_cols, num_rows, 1, gdal.GDT_Float32)
#     raster.GetRasterBand(1).WriteArray(save_array[n])
#     raster.GetRasterBand(1).SetNoDataValue(-32768)
#     raster.SetProjection(projection)
#     raster.SetGeoTransform(geotransform)
#     raster.FlushCache()
    
# print("running time: %s" % (time.time() - start_time))



import glob
import os
import numpy as np
from osgeo import gdal
from scipy.stats import linregress
import time

start_time = time.time()
MOD13A3Crop = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Crop"
tiffiles = glob.glob(MOD13A3Crop + '/' + '*.tif')
tiffiles = sorted(tiffiles)
years = np.arange(2015, 2020)

# Filter files in July
month = '07'
spectifs = []
for tiffile in tiffiles:
    monthstr = tiffile.split('.')[-3][-2:]
    if monthstr == month:
        spectifs.append(tiffile)

# Read filtered files and put them into a 3D array
images_list = []
for spectif in spectifs:
    raster = gdal.Open(spectif)
    geotransform = raster.GetGeoTransform()
    projection = raster.GetProjection()
    band = raster.GetRasterBand(1)
    image_array = band.ReadAsArray()
    images_list.append(image_array)

images_array_3d = np.array(images_list) / 1.0
images_array_3d[images_array_3d <= -3000] = np.nan
images_array_3d[images_array_3d >= 10000] = np.nan
images_array_3d = images_array_3d / 10000.0

num_rows, num_cols = images_array_3d[0].shape
slope_array = np.zeros((num_rows, num_cols))
slope_array[slope_array == 0] = np.nan

p_array = np.zeros((num_rows, num_cols))
p_array[p_array == 0] = np.nan

years = years.reshape(-1, 1)

# Conduct on each pixel
for i in range(num_rows):
    print(i)
    for j in range(num_cols):
        pixel_data = images_array_3d[:, i, j]
        nansize = np.size(np.where(np.isnan(pixel_data)))
        
        if nansize >= 0 and nansize <= 3:
            validIndex = np.where(~np.isnan(pixel_data))[0]
            
            if validIndex.size == 0:
                continue
            
            validIndex = validIndex[validIndex < years.size]  # Ensure validIndex is within range
            
            year_array1 = np.squeeze(years[validIndex])
            pixel_data1 = pixel_data[validIndex]
            
            if year_array1.size == 0 or pixel_data1.size == 0:
                continue       
            # Debug prints
            print(f"i: {i}, j: {j}, validIndex: {validIndex}, year_array1: {year_array1}, pixel_data1: {pixel_data1}")    
            # Linear regression
            slope, intercept, r_value, p_value, std_err = linregress(year_array1, pixel_data1)
            slope_array[i, j] = slope
            p_array[i, j] = p_value

slope_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\MODD13A3.008.Slope.tif'
p_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\TrendAnalysis\MODD13A3.008.Pvalue.tif'
save_path = [slope_path, p_path]
save_array = [slope_array, p_array]

for n in [0, 1]:
    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(save_path[n], num_cols, num_rows, 1, gdal.GDT_Float32)
    raster.GetRasterBand(1).WriteArray(save_array[n])
    raster.GetRasterBand(1).SetNoDataValue(-32768)
    raster.SetProjection(projection)
    raster.SetGeoTransform(geotransform)
    raster.FlushCache()

print("running time: %s" % (time.time() - start_time))
