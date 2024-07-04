import glob,os
import time
from osgeo import gdal
import numpy as np
from datetime import datetime

start_time = time.time()

pathrd = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Tif'
PATHWT = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD13\Merge'

layers = ["NDVI","EVI"]
years = range(2015,2021,1)

for layer in layers:
    layer = 'NDVI'
    for year in years:        
        print(year)
        wildcard = pathrd +'/' +'MOD13A3.A'+str(year)+"*" +".hdf_"+layer+".tif"
        print(wildcard)
        tiffiles = glob.glob(wildcard)        
        if np.size(tiffiles)>0:           
            juliandays = []
            for tiffile in tiffiles:
                #tiffile = tiffiles[0]
                julianday = tiffile.split('.')[1][-3:]
                juliandays.append(julianday)           
            juliandays = np.unique(juliandays)              
            for julianday in juliandays:            
                tiffiles_jld = []
                for tiffile in tiffiles:                 
                    julianday_ = tiffile.split('.')[1][-3:]
                    if julianday_ == julianday:
                        tiffiles_jld.append(tiffile)   
                        
                                        
                yearjulian = tiffiles_jld[0].split('.')[1][1:8]
                YearMonth = datetime.strptime(yearjulian,'%Y%j')            
                input_name = ''  
                for file in tiffiles_jld:
                    
                    input_name = input_name+' '+ file
                    
                input_name = input_name[1:]
                d = gdal.Open(tiffiles[0])
                nodata = d.GetRasterBand(1).GetNoDataValue()
                dtype = d.GetRasterBand(1).DataType
                dtype = gdal.GetDataTypeName(dtype)
                
                output_name = PATHWT +'\\'+"MOD13A3.A"+ str(year) + "{:02}".format(YearMonth.month)+"."+layer+".tif"  
                gdalmerge = r"python D:\Conda\Lib\site-packages\osgeo\utils\gdal_merge.py"
                command = ' '.join([gdalmerge,' -o', output_name, '-of GTiff -co COMPRESS=LZW -co BIGTIFF=YES', '-ot', dtype, '-n', str(nodata), '-a_nodata', str(nodata), input_name])
                os.system(command)

print("running time: %s" %(time.time() - start_time))