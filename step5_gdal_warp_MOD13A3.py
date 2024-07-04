import os,glob
import time
import re
from osgeo import gdal

s = os.sep

resolution = 0.01

pathrd = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Merge'
PATHWT = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Wrap"

tiffiles = glob.glob(pathrd + '/'+ '*.tif')

for tiffile in tiffiles:
    d = gdal.Open(tiffile)
    array_ = d.ReadAsArray()
    nodata = d.GetRasterBand(1).GetNoDataValue()
    # get data type name
    dtype = d.GetRasterBand(1).DataType
    dtype = gdal.GetDataTypeName(dtype)
    outputfile = PATHWT + s + os.path.basename(tiffile)
    print(outputfile)
    
    if not os.path.exists(outputfile):
        os.system('''gdalwarp -of GTIFF -overwrite -t_srs EPSG:4326'''+' -tr 0.01 0.01'+' -r near -co COMPRESS=LZW -co BIGTIFF=YES -ot'+' ' +dtype + ' -srcnodata ' + str(nodata)+' -dstnodata ' + str(nodata) + ' '+tiffile + ' ' +  outputfile)   
        