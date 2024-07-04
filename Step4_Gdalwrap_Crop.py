####cut the raster using shape
import glob,sys,os
#os.environ['PROJ_LIB'] = r'C:\Users\zhangwenjie\Anaconda3\Lib\site-packages\osgeo\data\proj'
from osgeo import gdal
import numpy as np
        
#%%for season surface presure 
Chinashp = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\Shp\Nanjing.shp"

MOD13A3Wrap = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Wrap"
MOD13A3Crop = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Crop"


tiffiles = glob.glob(MOD13A3Wrap + '/'+ '*.tif')

for tiffile in tiffiles:
        print(tiffile)
        filename = MOD13A3Crop +'\\' + tiffile.split('\\')[-1]
        crop = "gdalwarp -of GTiff -cutline "+ Chinashp + ' -cl '+ "Nanjing" +" -crop_to_cutline " +tiffile+ " " + filename
        os.system(crop)


