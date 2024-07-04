import glob,sys,os
from datetime import datetime, timedelta
import pandas as pd
from osgeo import gdal
import numpy as np
from pytz import timezone

#%%
def writeImageOut(outarray, outfile, dtype,gt,nodata):
    """"
    Output an image file:
    Array for output, Output file name and data type ( GDT_Byte, GDT_Int16, GDT_Float32, etc )
    """
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    
    outDs = driver.Create(outfile, outarray.shape[1], outarray.shape[0], 1, dtype)

    #print "rows and cols",cols,rows
    if outDs is None:
        print ('Could not create', outfile)
        sys.exit(1)
    outBand = outDs.GetRasterBand(1)
    outBand.WriteArray(outarray)
    outBand.SetNoDataValue(nodata)
    outDs.SetGeoTransform(gt)
    proj = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
    outDs.SetProjection(proj)
    outDs = None
    
#%%the average of seasonal-composited retrieved air temperature and surface pressure of five years
Monthly_composited_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge'

Pressure_Levels = [5,10,20,30,50,70,100,150,200,250,300,400,500,620,700,780,850,920]
sensors = ['MOD07']

overpasses = ['Day','Night']

seasons = ['Spring','Summer','Autumn','Winter']
for sensor in sensors:
    print(sensor)
    
    for overpass in overpasses:
        print(overpass)
        
        for pressure in Pressure_Levels:
            print(pressure)
            
            for season in seasons:
                print(season)
                seasonDomain_Array_pressure = np.zeros((2700,2700))
                seasonDomain_Array_pressure_Denominator = np.zeros((2700,2700))
               
                if season == 'Spring':
                    
                    MOD07_RTP_1 = sorted(glob.glob(Monthly_composited_path+sensor+'*'+'03'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_2 = sorted(glob.glob(Monthly_composited_path+'*'+'04'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_3 = sorted(glob.glob(Monthly_composited_path+'*'+'05'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                elif season == 'Summer':
                    MOD07_RTP_1 = sorted(glob.glob(Monthly_composited_path+'*'+'06'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_2 = sorted(glob.glob(Monthly_composited_path+'*'+'07'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_3 = sorted(glob.glob(Monthly_composited_path+'*'+'08'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                elif season == 'Autumn':
                    MOD07_RTP_1 = sorted(glob.glob(Monthly_composited_path+'*'+'09'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_2 = sorted(glob.glob(Monthly_composited_path+'*'+'10'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_3 = sorted(glob.glob(Monthly_composited_path+'*'+'11'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                else:
                    MOD07_RTP_1 = sorted(glob.glob(Monthly_composited_path+'*'+'12'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_2 = sorted(glob.glob(Monthly_composited_path+'*'+'01'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                    MOD07_RTP_3 = sorted(glob.glob(Monthly_composited_path+'*'+'02'+'_'+overpass+'_'+str(pressure)+'hpa.tif'))
                
                MOD07_RTPs = MOD07_RTP_1 + MOD07_RTP_2 + MOD07_RTP_3
                
                for MOD07_RTP in MOD07_RTPs:
                    TifPath = glob.glob(os.path.join('D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge' + '*.tif'))
                    for TifPath in TifPath:
                        Tile_MOD07_RTP = gdal.Open(TifPath)
                        Tile_MOD07RTP_cols = Tile_MOD07_RTP.RasterXSize
                        Tile_MOD07RTP_rows = Tile_MOD07_RTP.RasterYSize
                        Tile_MOD07RTP_heights = Tile_MOD07_RTP.RasterZsize
                        
                        Tile_GeoTransform = Tile_MOD07_RTP.GetGeoTransform()
                        Tile_MOD07_RTP_data = Tile_MOD07_RTP.ReadAsArray()
                        Tile_MOD07_RTP_data[np.isnan(Tile_MOD07_RTP_data)]=0
                        np.unique(Tile_MOD07_RTP_data)
                        Tile_MOD07_RTP_data.shape
                        V10201 = np.where(Tile_MOD07_RTP_data==10201)
                        Tile_MOD07_RTP_data[V10201[0][0][0],V10201[1][0][0]]
                        Nlat = 90
                        Slat = 90
                        Elon = 145
                        Wlon = 45
                        Empty_Array = np.zeros((1800,2000))*np.nan
                        print(Empty_Array)
                        xOffset = abs(int((45-Tile_GeoTransform[0])/0.05))
                        yOffset = abs(int((90-Tile_GeoTransform[3])/0.05))
                        Empty_Array[yOffset:yOffset + Tile_MOD07_RTP_data.shape[1], xOffset:xOffset + Tile_MOD07_RTP_data.shape[1]] = Tile_MOD07_RTP_data
                        seasonDomain_Array_pressure = seasonDomain_Array_pressure + Tile_MOD07_RTP_data   
                        Tile_MOD07_RTP_data[Tile_MOD07_RTP_data!=0]=1
                        seasonDomain_Array_pressure_Denominator = seasonDomain_Array_pressure_Denominator + Tile_MOD07_RTP_data
                
                    seasonDomain_Array_pressure_Denominator[seasonDomain_Array_pressure_Denominator==0]=np.nan    
                    seasonDomain_Array_Average = seasonDomain_Array_pressure/seasonDomain_Array_pressure_Denominator
                
                    noData = -32768
                    pixel = Tile_GeoTransform[1]
                    geot = Tile_GeoTransform
                    dtype = gdal.GDT_Float32
                
                    outputpath = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge"
                    fullpath = outputpath + sensor +"_L2_RetrieveTa_"+season+'_' + overpass+'_'+str(pressure)+'hpa.tif'
                    writeImageOut(seasonDomain_Array_Average, fullpath, dtype, geot,noData)

# %%
