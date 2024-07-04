import glob,sys,os
from datetime import datetime, timedelta
import pandas as pd
from osgeo import gdal
import numpy as np
import matplotlib
from osgeo import gdal_array
from pytz import timezone
from osgeo import gdal

def writeImageOut(outarray, outfile, dtype,gt,nodata):
    """"
    Output an image file:
    Array for output, Output file name and data type ( GDT_Byte, GDT_Int16, GDT_Float32, etc )
    """
    outarray[np.isnan(outarray)]=-32768
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    
    outDs = driver.Create(outfile, outarray.shape[2], outarray.shape[1], 20, dtype)

    #print "rows and cols",cols,rows
    if outDs is None:
        print ('Could not create', outfile)
        sys.exit(1)
    for i,image in enumerate(outarray,1):
        print(i)
        print(image.shape)
        outDs.GetRasterBand(i).WriteArray(image)  
        outDs.GetRasterBand(i).SetNoDataValue(nodata)
    outDs.SetGeoTransform(gt)
    proj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
    outDs.SetProjection(proj)
    outDs.FlushCache() 
    outDs = None

#%%
def checkallgreater(list1, val):
    return(all(x > val for x in list1))

def checkallsmaller(list1, val):
    return(all(x < val for x in list1))
#%%
jsonpath = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\HDF'
json_files = glob.glob(jsonpath + "*.hdf")
tip_file =r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF'
#print (json_files)

for jsonfile in json_files:
    #print (jsonfile[:-4])
    jsonfile_name=jsonfile.split('\\')[-1].split('h')[0]+'.tif'#获得名称
    hdf = gdal.Open(jsonfile,gdal.GA_ReadOnly)
    hdf_metadata = hdf.GetMetadata()

    hdf_Sub = hdf.GetSubDatasets()
    inputname_sf = hdf_Sub[14][0]
    #outputname_sf = os.path.join(jsonfile[:-4])+'.tif'
    outputname_sf= tip_file+jsonfile_name #修改路径和名称
    os.system("gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326"+' -tr 0.05 0.05'+' -r near'+' ' + inputname_sf + ' ' +  outputname_sf)
        
Nlat=90
Slat=0
Elon=145
Wlon=45
Empty_Arrary=np.zeros((20,1800,2000))*np.nan
Empty_Arrary1=np.zeros((20,1800,2000))*np.nan
tip_file =r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF'
json_files1 = glob.glob(tip_file + "*.tif")
i=0
#TifPATH='E:/ly_3down/python/pyt_1/temp/mod07_l2_tif/MOD07_L2.A2024061.1415.061.2024062011714_2025.tif'
for file in json_files1:
    i=i+1
    Tile_MOD07_RTP = gdal.Open(file) 
    Tile_cols = Tile_MOD07_RTP.RasterXSize
    Tile_rows = Tile_MOD07_RTP.RasterYSize
    Tile_GeoTransform = Tile_MOD07_RTP.GetGeoTransform()#左上角经纬度信息和空间分辨率
    Tile_MOD07_RTP_data = Tile_MOD07_RTP.ReadAsArray()/1.0
    np.unique(Tile_MOD07_RTP_data)
    Tile_MOD07_RTP_data.shape
    np.nanmax(Tile_MOD07_RTP_data)
    #np.where(Tile_MOD07_RTP_data==10212)#获得行列号

    xOffset = abs(int((45-Tile_GeoTransform[0]) / 0.05))
    yOffset = abs(int((90-Tile_GeoTransform[3]) / 0.05))
    
    if i>1:
        Empty_Arrary1[0:20,yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]]=Tile_MOD07_RTP_data
        #Empty_Arrary_c = Empty_Arrary.copy()
        Empty_Arrary[np.isnan(Empty_Arrary)] = 0
        Empty_Arrary1[np.isnan(Empty_Arrary1)] = 0#nan->0
        
        Empty_Arrary[np.where(Empty_Arrary<0)]=0
        Empty_Arrary1[np.where(Empty_Arrary1<0)]=0#-32768->0
        
        Empty_ArraryA=Empty_Arrary+Empty_Arrary1#分子
        np.unique(Empty_ArraryA)
        
        
        Empty_Arrary[np.where(Empty_Arrary>0)]=1
        Empty_Arrary1[np.where(Empty_Arrary1>0)]=1
        Empty_ArraryB=Empty_Arrary+Empty_Arrary1
        Empty_ArraryB[Empty_ArraryB==0]=np.nan#分母

        
        Empty_Arrary=Empty_ArraryA/Empty_ArraryB
    else:
        Empty_Arrary[0:20,yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]]=Tile_MOD07_RTP_data
        

np.unique(Empty_Arrary)
GeoTransform=(45.0, 0.05, 0.0, 90.0, 0.0, -0.05)
noData=-32768
pixel=GeoTransform[1]
geot=GeoTransform
dtype=gdal.GDT_Float32
tip_file_ =r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge'#保存路径
writeImageOut(Empty_Arrary,tip_file_,dtype,geot,noData)


