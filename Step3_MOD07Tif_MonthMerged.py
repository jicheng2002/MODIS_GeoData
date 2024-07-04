#!/usr/bin/env python
# -*- coding: utf-8 -*-
####check if the mod07 have the ability to depict the mountain effect. 
####5, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 620, 700, 780, 850, 920, 950, and 1000 hpa

import glob,sys,os
from datetime import datetime, timedelta
import pandas as pd
from osgeo import gdal
import numpy as np
import matplotlib
from osgeo import gdal_array
from pytz import timezone

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
    
#%% daily and month-composited retrieved air temperature and surface pressure of each year
    
Pressure_Levels = [5,10,20,30,50,70,100,150,200,250,300,400,500,620,700,780,850,920,950,1000]
sensors = ['MOD07']
overpasses = ['Day','Night']
years = ['2022','2023']
Tif_Path_MOD07 = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF'

for sensor in sensors:
    print(sensor)
    
    for year in years:
        print(year)
        
        for overpass in overpasses:
            print(overpass)
            
            Tif_Path_MOD07path = Tif_Path_MOD07+'/'+year+'/'+overpass+'/'
            Tif_Files_MOD07_RTP = glob.glob(Tif_Path_MOD07path+'*.tif')
            
            TifPath = glob.glob(os.path.join('D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF' + '*.tif'))
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
                Empty_Array = np.zeros((20,1800,2000))*np.nan
                print(Empty_Array)
                xOffset = abs(int((45-Tile_GeoTransform[0])/0.05))
                yOffset = abs(int((90-Tile_GeoTransform[3])/0.05))
                
                Empty_Array[yOffset:yOffset + Tile_MOD07_RTP_data.shape[1], xOffset:xOffset + Tile_MOD07_RTP_data.shape[1]] = Tile_MOD07_RTP_data


            for month in range(1,13):
                if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    
                    strptime1 = year + '-' + "{:02d}".format(month) + '-' + '01'
                    strptime2 = year + '-' + "{:02d}".format(month) + '-' + '31'
                elif month == 4 or month == 6 or month == 9 or month == 11:
                    strptime1 = year + '-' + "{:02d}".format(month) + '-' + '01'
                    strptime2 = year + '-' + "{:02d}".format(month) + '-' + '30'
                else:
                    strptime1 = year + '-' + "{:02d}".format(month) + '-' + '01'
                    strptime2 = year + '-' + "{:02d}".format(month) + '-' + '28'
                
                start = datetime.strptime(strptime1, "%Y-%m-%d")
                end = datetime.strptime(strptime2, "%Y-%m-%d")
                date_generated = [start + timedelta(days=x) for x in range(0, ((end-start).days+1))]
                #print(date_generated)
              
                MonthDomain_Array_5hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_10hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_20hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_30hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_50hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_70hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_100hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_150hpa_Day = np.zeros((2700,2700))
                
                MonthDomain_Array_200hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_250hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_300hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_400hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_500hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_620hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_700hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_780hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_850hpa_Day = np.zeros((2700,2700))
                MonthDomain_Array_920hpa_Day = np.zeros((2700,2700))
                
                ###*******###
                MonthDomain_Array_5hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_10hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_20hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_30hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_50hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_70hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_100hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_150hpa_DayDenominator = np.zeros((2700,2700))
                
                MonthDomain_Array_200hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_250hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_300hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_400hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_500hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_620hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_700hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_780hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_850hpa_DayDenominator = np.zeros((2700,2700))
                MonthDomain_Array_920hpa_DayDenominator = np.zeros((2700,2700))
                #####daily systhetic 
                for date in date_generated:
                    month_day= date.strftime("%Y-%m-%d")
                    print(month_day)
                    DailyDomain_Array_5hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_10hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_20hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_30hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_50hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_70hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_100hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_150hpa_Day = np.zeros((2700,2700))
                    
                    DailyDomain_Array_200hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_250hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_300hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_400hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_500hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_620hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_700hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_780hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_850hpa_Day = np.zeros((2700,2700))
                    DailyDomain_Array_920hpa_Day = np.zeros((2700,2700))
                    
                    ####****####
                    DailyDomain_Array_5hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_10hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_20hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_30hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_50hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_70hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_100hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_150hpa_DayDenominator = np.zeros((2700,2700))
                   
                    DailyDomain_Array_200hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_250hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_300hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_400hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_500hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_620hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_700hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_780hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_850hpa_DayDenominator = np.zeros((2700,2700))
                    DailyDomain_Array_920hpa_DayDenominator = np.zeros((2700,2700))
                    
                    for i in range(0,np.size(Tif_Files_MOD07_RTP)):
                        yearjulian = Tif_Files_MOD07_RTP[i].split('.')[1][1:8]
                        YearMonth = datetime.strptime(yearjulian,'%Y%j')
                        hour = Tif_Files_MOD07_RTP[i].split('.')[2][0:2]
                        minutes= Tif_Files_MOD07_RTP[i].split('.')[2][2:4]
                        #Date_MOD07_ToMins = datetime(year = YearMonth.year,month = YearMonth.month,day=YearMonth.day,hour=int(hour),minute=int(minutes))
                        Date_MOD07_ToDay = datetime(year = YearMonth.year,month = YearMonth.month,day=YearMonth.day)
                        Date_MOD07_ToDayStrftime = Date_MOD07_ToDay.strftime("%Y-%m-%d") 
                        if Date_MOD07_ToDayStrftime == month_day:
                            Date_MOD07_ToMins = datetime(year = YearMonth.year,month = YearMonth.month,day=YearMonth.day,hour=int(hour),minute=int(minutes))
                            #MOD07_Time_Daily.appSend( Date_MOD07_Moment)
                            #MOD07_Tif_List_Daily_SP.append(Tif_Files_MOD07_SP[i])
                            #MOD07_Tif_List_Daily_RTP.append(Tif_Files_MOD07_RTP[i])
                            #Tif_Name_SP = Tif_Files_MOD07_SP[i].split('/')[7]
                            Tif_Name_RTP = Tif_Files_MOD07_RTP[i].split('\\')[1]
                            #output_name_SP = '/Volumes/Macintosh2TBHD/Wenjie_Sci/GitHub/TemperatureEstimation/ValidationOfMOD07/NewResults/TemporalResample/MOD07/'+Tif_Name_SP
                            #output_name_RTP = '/Volumes/UTS2/UTSMacintosh2Part2/Wenjie_Sci/GitHub/MountainEffect/MOD07DailyComposited5000km/'+ Tif_Name_RTP
                            #os.system("gdal_merge.py -of GTIFF -n -32768 -ps 0.05 0.05 -o"+' ' + output_name_SP + ' ' + Tif_Files_MOD07_SP[i])
                            #sys.stdout.flush()
                            #os.system("gdal_merge.py -of GTIFF -n -32768 -ps 0.05 0.05 -o"+' ' + output_name_RTP + ' ' + Tif_Files_MOD07_RTP[i])
                            #sys.stdout.flush()
                            Tile_MOD07_RTP = gdal.Open(Tif_Files_MOD07_RTP[i]) 
                            Tile_MOD07RTP_cols = Tile_MOD07_RTP.RasterXSize
                            Tile_MOD07RTP_rows = Tile_MOD07_RTP.RasterYSize
                            Tile_GeoTransform = Tile_MOD07_RTP.GetGeoTransform()
                            Tile_MOD07_RTP_data = Tile_MOD07_RTP.ReadAsArray()/1.0
                            Tile_MOD07_RTP_data[Tile_MOD07_RTP_data==-32768]=0
                       
                            xOffset = abs(int((45-Tile_GeoTransform[0]) / 0.05))
                            yOffset = abs(int((90-Tile_GeoTransform[3]) / 0.05))
                            

                    
                #            o=ephem.Observer() ###observation
                #            o.lat=str(Tile_GeoTransform[4])
                #            #print(Site_Tile[u'纬度'].iloc[site])
                #            o.lon = str(Tile_GeoTransform[0])
                #            #print(Site_Tile[u'经度'].iloc[site])
                #            o.date = str(Date_MOD07_ToDay )
                #            s=ephem.Sun()
                #            s.compute(o)
                #            DateRise = (datetime.strptime(str(o.previous_rising(s)), "%Y/%m/%d %H:%M:%S"))
                #            DateSet = (datetime.strptime(str(o.next_setting(s)), "%Y/%m/%d %H:%M:%S"))
                            
                            if ((Tile_MOD07_RTP_data.shape[1] + yOffset) <2700)&((xOffset+Tile_MOD07_RTP_data.shape[2])<2700):
                                #if (Date_MOD07_ToMins>DateRise and Date_MOD07_ToMins<DateSet):
                                    #print("daytime")
                                    #print Tif_Files_MOD07_RTP[i]
                                Domain_Array_5hpa_Day = np.zeros((2700,2700))
                                Domain_Array_10hpa_Day = np.zeros((2700,2700))
                                Domain_Array_20hpa_Day = np.zeros((2700,2700))
                                Domain_Array_30hpa_Day = np.zeros((2700,2700))
                                Domain_Array_50hpa_Day = np.zeros((2700,2700))
                                Domain_Array_70hpa_Day = np.zeros((2700,2700))
                                Domain_Array_100hpa_Day = np.zeros((2700,2700))
                                Domain_Array_150hpa_Day = np.zeros((2700,2700))
                                
                                Domain_Array_200hpa_Day = np.zeros((2700,2700))
                                Domain_Array_250hpa_Day = np.zeros((2700,2700))
                                Domain_Array_300hpa_Day = np.zeros((2700,2700))
                                Domain_Array_400hpa_Day = np.zeros((2700,2700))
                                Domain_Array_500hpa_Day = np.zeros((2700,2700))
                                Domain_Array_620hpa_Day = np.zeros((2700,2700))
                                Domain_Array_700hpa_Day = np.zeros((2700,2700))
                                Domain_Array_780hpa_Day = np.zeros((2700,2700))
                                Domain_Array_850hpa_Day = np.zeros((2700,2700))
                                Domain_Array_920hpa_Day = np.zeros((2700,2700))
                                Domain_Array_First_Pressure_Day = np.zeros((2700,2700))
                                Domain_Array_Second_Pressure_Day = np.zeros((2700,2700))
                                Domain_Array_SP_Day = np.zeros((2700,2700))
                                Domain_GeoTransform = (45, 0.05, 0.0, 90.0, 0.0, -0.05)
                                #5,10,20,30,50,70,100,150,200,250,300,400,500,620,700,780,850,920,950,1000
                                Layer5hpa = Tile_MOD07_RTP_data[0,:,:]
                                Layer10hpa = Tile_MOD07_RTP_data[1,:,:]
                                Layer20hpa = Tile_MOD07_RTP_data[2,:,:]
                                Layer30hpa = Tile_MOD07_RTP_data[3,:,:]
                                Layer50hpa = Tile_MOD07_RTP_data[4,:,:]
                                Layer70hpa = Tile_MOD07_RTP_data[5,:,:]
                                Layer100hpa = Tile_MOD07_RTP_data[6,:,:]
                                Layer150hpa = Tile_MOD07_RTP_data[7,:,:]
                                
                                Layer200hpa = Tile_MOD07_RTP_data[8,:,:]
                                Layer250hpa = Tile_MOD07_RTP_data[9,:,:]
                                Layer300hpa = Tile_MOD07_RTP_data[10,:,:]
                                Layer400hpa = Tile_MOD07_RTP_data[11,:,:]
                                Layer500hpa = Tile_MOD07_RTP_data[12,:,:]
                                Layer620hpa = Tile_MOD07_RTP_data[13,:,:]
                                Layer700hpa = Tile_MOD07_RTP_data[14,:,:]
                                Layer780hpa = Tile_MOD07_RTP_data[15,:,:]
                                Layer850hpa = Tile_MOD07_RTP_data[16,:,:]
                                Layer920hpa = Tile_MOD07_RTP_data[17,:,:]
                                
                                Layer5hpa[Layer5hpa==0]=np.nan
                                Layer10hpa[Layer10hpa==0]=np.nan
                                Layer20hpa[Layer20hpa==0]=np.nan
                                Layer30hpa[Layer30hpa==0]=np.nan
                                Layer50hpa[Layer50hpa==0]=np.nan
                                Layer70hpa[Layer70hpa==0]=np.nan
                                Layer100hpa[Layer100hpa==0]=np.nan
                                Layer150hpa[Layer150hpa==0]=np.nan
                                
                                Layer200hpa[Layer200hpa==0]=np.nan
                                Layer250hpa[Layer250hpa==0]=np.nan
                                Layer300hpa[Layer300hpa==0]=np.nan
                                Layer400hpa[Layer400hpa==0]=np.nan
                                Layer500hpa[Layer500hpa==0]=np.nan
                                Layer620hpa[Layer620hpa==0]=np.nan
                                Layer700hpa[Layer700hpa==0]=np.nan
                                Layer780hpa[Layer780hpa==0]=np.nan
                                Layer850hpa[Layer850hpa==0]=np.nan
                                Layer920hpa[Layer920hpa==0]=np.nan
                                
                                ###****###
                                
                                Domain_Array_5hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer5hpa+15000)*0.01-273.16
                                Domain_Array_10hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer10hpa+15000)*0.01-273.16
                                Domain_Array_20hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer20hpa+15000)*0.01-273.16
                                Domain_Array_30hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer30hpa+15000)*0.01-273.16
                                Domain_Array_50hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer50hpa+15000)*0.01-273.16
                                Domain_Array_70hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer70hpa+15000)*0.01-273.16
                                Domain_Array_100hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer100hpa+15000)*0.01-273.16
                                Domain_Array_150hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer150hpa+15000)*0.01-273.16
                                
                                Domain_Array_200hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer200hpa+15000)*0.01-273.16
                                Domain_Array_250hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer250hpa+15000)*0.01-273.16
                                Domain_Array_300hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer300hpa+15000)*0.01-273.16
                                Domain_Array_400hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer400hpa+15000)*0.01-273.16
                                Domain_Array_500hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer500hpa+15000)*0.01-273.16
                                Domain_Array_620hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer620hpa+15000)*0.01-273.16
                                Domain_Array_700hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer700hpa+15000)*0.01-273.16
                                Domain_Array_780hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer780hpa+15000)*0.01-273.16
                                Domain_Array_850hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer850hpa+15000)*0.01-273.16
                                Domain_Array_920hpa_Day[yOffset:yOffset+Tile_MOD07_RTP_data.shape[1],xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = (Layer920hpa+15000)*0.01-273.16
                                
                                ###****####
                                Domain_Array_5hpa_Day[np.isnan(Domain_Array_5hpa_Day)]=0
                                Domain_Array_10hpa_Day[np.isnan(Domain_Array_10hpa_Day)]=0
                                Domain_Array_20hpa_Day[np.isnan(Domain_Array_20hpa_Day)]=0
                                Domain_Array_30hpa_Day[np.isnan(Domain_Array_30hpa_Day)]=0
                                Domain_Array_50hpa_Day[np.isnan(Domain_Array_50hpa_Day)]=0
                                Domain_Array_70hpa_Day[np.isnan(Domain_Array_70hpa_Day)]=0
                                Domain_Array_100hpa_Day[np.isnan(Domain_Array_100hpa_Day)]=0
                                Domain_Array_150hpa_Day[np.isnan(Domain_Array_150hpa_Day)]=0
                                
                                Domain_Array_200hpa_Day[np.isnan(Domain_Array_200hpa_Day)]=0
                                Domain_Array_250hpa_Day[np.isnan(Domain_Array_250hpa_Day)]=0
                                Domain_Array_300hpa_Day[np.isnan(Domain_Array_300hpa_Day)]=0
                                Domain_Array_400hpa_Day[np.isnan(Domain_Array_400hpa_Day)]=0
                                Domain_Array_500hpa_Day[np.isnan(Domain_Array_500hpa_Day)]=0
                                Domain_Array_620hpa_Day[np.isnan(Domain_Array_620hpa_Day)]=0
                                Domain_Array_700hpa_Day[np.isnan(Domain_Array_700hpa_Day)]=0
                                Domain_Array_780hpa_Day[np.isnan(Domain_Array_780hpa_Day)]=0
                                Domain_Array_850hpa_Day[np.isnan(Domain_Array_850hpa_Day)]=0
                                Domain_Array_920hpa_Day[np.isnan(Domain_Array_920hpa_Day)]=0
                                
                                ###***###
                                DailyDomain_Array_5hpa_Day = DailyDomain_Array_5hpa_Day + Domain_Array_5hpa_Day
                                DailyDomain_Array_10hpa_Day = DailyDomain_Array_10hpa_Day + Domain_Array_10hpa_Day
                                DailyDomain_Array_20hpa_Day = DailyDomain_Array_20hpa_Day + Domain_Array_20hpa_Day
                                DailyDomain_Array_30hpa_Day = DailyDomain_Array_30hpa_Day + Domain_Array_30hpa_Day
                                DailyDomain_Array_50hpa_Day = DailyDomain_Array_50hpa_Day + Domain_Array_50hpa_Day
                                DailyDomain_Array_70hpa_Day = DailyDomain_Array_70hpa_Day + Domain_Array_70hpa_Day
                                DailyDomain_Array_100hpa_Day = DailyDomain_Array_100hpa_Day + Domain_Array_100hpa_Day
                                DailyDomain_Array_150hpa_Day = DailyDomain_Array_150hpa_Day + Domain_Array_150hpa_Day
                                
                                DailyDomain_Array_200hpa_Day = DailyDomain_Array_200hpa_Day + Domain_Array_200hpa_Day
                                DailyDomain_Array_250hpa_Day = DailyDomain_Array_250hpa_Day + Domain_Array_250hpa_Day
                                DailyDomain_Array_300hpa_Day = DailyDomain_Array_300hpa_Day + Domain_Array_300hpa_Day
                                DailyDomain_Array_400hpa_Day = DailyDomain_Array_400hpa_Day + Domain_Array_400hpa_Day
                                DailyDomain_Array_500hpa_Day = DailyDomain_Array_500hpa_Day + Domain_Array_500hpa_Day
                                DailyDomain_Array_620hpa_Day = DailyDomain_Array_620hpa_Day + Domain_Array_620hpa_Day
                                DailyDomain_Array_700hpa_Day = DailyDomain_Array_700hpa_Day + Domain_Array_700hpa_Day
                                DailyDomain_Array_780hpa_Day = DailyDomain_Array_780hpa_Day + Domain_Array_780hpa_Day
                                DailyDomain_Array_850hpa_Day = DailyDomain_Array_850hpa_Day + Domain_Array_850hpa_Day
                                DailyDomain_Array_920hpa_Day = DailyDomain_Array_920hpa_Day + Domain_Array_920hpa_Day
                                
                                
                                Domain_Array_5hpa_Day[Domain_Array_5hpa_Day!=0]=1
                                Domain_Array_10hpa_Day[Domain_Array_10hpa_Day!=0]=1
                                Domain_Array_20hpa_Day[Domain_Array_20hpa_Day!=0]=1
                                Domain_Array_30hpa_Day[Domain_Array_30hpa_Day!=0]=1
                                Domain_Array_50hpa_Day[Domain_Array_50hpa_Day!=0]=1
                                Domain_Array_70hpa_Day[Domain_Array_70hpa_Day!=0]=1
                                Domain_Array_100hpa_Day[Domain_Array_100hpa_Day!=0]=1
                                Domain_Array_150hpa_Day[Domain_Array_150hpa_Day!=0]=1
                                
                                Domain_Array_200hpa_Day[Domain_Array_200hpa_Day!=0]=1
                                Domain_Array_250hpa_Day[Domain_Array_250hpa_Day!=0]=1
                                Domain_Array_300hpa_Day[Domain_Array_300hpa_Day!=0]=1
                                Domain_Array_400hpa_Day[Domain_Array_400hpa_Day!=0]=1
                                Domain_Array_500hpa_Day[Domain_Array_500hpa_Day!=0]=1
                                Domain_Array_620hpa_Day[Domain_Array_620hpa_Day!=0]=1
                                Domain_Array_700hpa_Day[Domain_Array_700hpa_Day!=0]=1
                                Domain_Array_780hpa_Day[Domain_Array_780hpa_Day!=0]=1
                                Domain_Array_850hpa_Day[Domain_Array_850hpa_Day!=0]=1
                                Domain_Array_920hpa_Day[Domain_Array_920hpa_Day!=0]=1
                                
                                
                                DailyDomain_Array_5hpa_DayDenominator = DailyDomain_Array_5hpa_DayDenominator + Domain_Array_5hpa_Day
                                DailyDomain_Array_10hpa_DayDenominator = DailyDomain_Array_10hpa_DayDenominator + Domain_Array_10hpa_Day
                                DailyDomain_Array_20hpa_DayDenominator = DailyDomain_Array_20hpa_DayDenominator + Domain_Array_20hpa_Day
                                DailyDomain_Array_30hpa_DayDenominator = DailyDomain_Array_30hpa_DayDenominator + Domain_Array_30hpa_Day
                                DailyDomain_Array_50hpa_DayDenominator = DailyDomain_Array_50hpa_DayDenominator + Domain_Array_50hpa_Day
                                DailyDomain_Array_70hpa_DayDenominator = DailyDomain_Array_70hpa_DayDenominator + Domain_Array_70hpa_Day
                                DailyDomain_Array_100hpa_DayDenominator = DailyDomain_Array_100hpa_DayDenominator + Domain_Array_100hpa_Day
                                DailyDomain_Array_150hpa_DayDenominator = DailyDomain_Array_150hpa_DayDenominator + Domain_Array_150hpa_Day
                                
                                DailyDomain_Array_200hpa_DayDenominator = DailyDomain_Array_200hpa_DayDenominator + Domain_Array_200hpa_Day
                                DailyDomain_Array_250hpa_DayDenominator = DailyDomain_Array_250hpa_DayDenominator + Domain_Array_250hpa_Day
                                DailyDomain_Array_300hpa_DayDenominator = DailyDomain_Array_300hpa_DayDenominator + Domain_Array_300hpa_Day
                                DailyDomain_Array_400hpa_DayDenominator = DailyDomain_Array_400hpa_DayDenominator + Domain_Array_400hpa_Day
                                DailyDomain_Array_500hpa_DayDenominator = DailyDomain_Array_500hpa_DayDenominator + Domain_Array_500hpa_Day
                                DailyDomain_Array_620hpa_DayDenominator = DailyDomain_Array_620hpa_DayDenominator + Domain_Array_620hpa_Day
                                DailyDomain_Array_700hpa_DayDenominator = DailyDomain_Array_700hpa_DayDenominator + Domain_Array_700hpa_Day
                                DailyDomain_Array_780hpa_DayDenominator = DailyDomain_Array_780hpa_DayDenominator + Domain_Array_780hpa_Day
                                DailyDomain_Array_850hpa_DayDenominator = DailyDomain_Array_850hpa_DayDenominator + Domain_Array_850hpa_Day
                                DailyDomain_Array_920hpa_DayDenominator = DailyDomain_Array_920hpa_DayDenominator + Domain_Array_920hpa_Day
                                Tile_MOD07_RTP = None 
                                
                                #Tile_MOD07_SP = None
                    
                    MonthDomain_Array_5hpa_Day = MonthDomain_Array_5hpa_Day + DailyDomain_Array_5hpa_Day
                    MonthDomain_Array_10hpa_Day = MonthDomain_Array_10hpa_Day + DailyDomain_Array_10hpa_Day
                    MonthDomain_Array_20hpa_Day = MonthDomain_Array_20hpa_Day + DailyDomain_Array_20hpa_Day
                    MonthDomain_Array_30hpa_Day = MonthDomain_Array_30hpa_Day + DailyDomain_Array_30hpa_Day
                    MonthDomain_Array_50hpa_Day = MonthDomain_Array_50hpa_Day + DailyDomain_Array_50hpa_Day
                    MonthDomain_Array_70hpa_Day = MonthDomain_Array_70hpa_Day + DailyDomain_Array_70hpa_Day
                    MonthDomain_Array_100hpa_Day = MonthDomain_Array_100hpa_Day + DailyDomain_Array_100hpa_Day
                    MonthDomain_Array_150hpa_Day = MonthDomain_Array_150hpa_Day + DailyDomain_Array_150hpa_Day
                    
                    MonthDomain_Array_200hpa_Day = MonthDomain_Array_200hpa_Day + DailyDomain_Array_200hpa_Day
                    MonthDomain_Array_250hpa_Day = MonthDomain_Array_250hpa_Day + DailyDomain_Array_250hpa_Day
                    MonthDomain_Array_300hpa_Day = MonthDomain_Array_300hpa_Day + DailyDomain_Array_300hpa_Day
                    MonthDomain_Array_400hpa_Day = MonthDomain_Array_400hpa_Day + DailyDomain_Array_400hpa_Day
                    MonthDomain_Array_500hpa_Day = MonthDomain_Array_500hpa_Day + DailyDomain_Array_500hpa_Day
                    MonthDomain_Array_620hpa_Day = MonthDomain_Array_620hpa_Day + DailyDomain_Array_620hpa_Day
                    MonthDomain_Array_700hpa_Day = MonthDomain_Array_700hpa_Day + DailyDomain_Array_700hpa_Day
                    MonthDomain_Array_780hpa_Day = MonthDomain_Array_780hpa_Day + DailyDomain_Array_780hpa_Day
                    MonthDomain_Array_850hpa_Day = MonthDomain_Array_850hpa_Day + DailyDomain_Array_850hpa_Day
                    MonthDomain_Array_920hpa_Day = MonthDomain_Array_920hpa_Day + DailyDomain_Array_920hpa_Day
                    
                    ###*****####
                    MonthDomain_Array_5hpa_DayDenominator = MonthDomain_Array_5hpa_DayDenominator + DailyDomain_Array_5hpa_DayDenominator
                    MonthDomain_Array_10hpa_DayDenominator = MonthDomain_Array_10hpa_DayDenominator + DailyDomain_Array_10hpa_DayDenominator
                    MonthDomain_Array_20hpa_DayDenominator = MonthDomain_Array_20hpa_DayDenominator + DailyDomain_Array_20hpa_DayDenominator
                    MonthDomain_Array_30hpa_DayDenominator = MonthDomain_Array_30hpa_DayDenominator + DailyDomain_Array_30hpa_DayDenominator
                    MonthDomain_Array_50hpa_DayDenominator = MonthDomain_Array_50hpa_DayDenominator + DailyDomain_Array_50hpa_DayDenominator
                    MonthDomain_Array_70hpa_DayDenominator = MonthDomain_Array_70hpa_DayDenominator + DailyDomain_Array_70hpa_DayDenominator
                    MonthDomain_Array_100hpa_DayDenominator = MonthDomain_Array_100hpa_DayDenominator + DailyDomain_Array_100hpa_DayDenominator
                    MonthDomain_Array_150hpa_DayDenominator = MonthDomain_Array_150hpa_DayDenominator + DailyDomain_Array_150hpa_DayDenominator
                    
                    MonthDomain_Array_200hpa_DayDenominator = MonthDomain_Array_200hpa_DayDenominator + DailyDomain_Array_200hpa_DayDenominator
                    MonthDomain_Array_250hpa_DayDenominator = MonthDomain_Array_250hpa_DayDenominator + DailyDomain_Array_250hpa_DayDenominator
                    MonthDomain_Array_300hpa_DayDenominator = MonthDomain_Array_300hpa_DayDenominator + DailyDomain_Array_300hpa_DayDenominator
                    MonthDomain_Array_400hpa_DayDenominator = MonthDomain_Array_400hpa_DayDenominator + DailyDomain_Array_400hpa_DayDenominator
                    MonthDomain_Array_500hpa_DayDenominator = MonthDomain_Array_500hpa_DayDenominator + DailyDomain_Array_500hpa_DayDenominator
                    MonthDomain_Array_620hpa_DayDenominator = MonthDomain_Array_620hpa_DayDenominator + DailyDomain_Array_620hpa_DayDenominator
                    MonthDomain_Array_700hpa_DayDenominator = MonthDomain_Array_700hpa_DayDenominator + DailyDomain_Array_700hpa_DayDenominator
                    MonthDomain_Array_780hpa_DayDenominator = MonthDomain_Array_780hpa_DayDenominator + DailyDomain_Array_780hpa_DayDenominator
                    MonthDomain_Array_850hpa_DayDenominator = MonthDomain_Array_850hpa_DayDenominator + DailyDomain_Array_850hpa_DayDenominator
                    MonthDomain_Array_920hpa_DayDenominator = MonthDomain_Array_920hpa_DayDenominator + DailyDomain_Array_920hpa_DayDenominator
                    
                    # noData = -32768
                    # pixel = Domain_GeoTransform[1]
                    # geot = Domain_GeoTransform
                    # dtype = gdal.GDT_Float32
    #                
    #                DailyDomain_Array_500hpa_DayDenominator[DailyDomain_Array_500hpa_DayDenominator==0]=np.nan
    #                DailyDomain_Array_500hpa_DayAverage = DailyDomain_Array_500hpa_Day/DailyDomain_Array_500hpa_DayDenominator
    #                outputpath = "/Users/wenjiezhang/Research/Paper-Research/MountainEffect/Results/TIF/DailyComposite/"
    #                
    #                Layer500hpaDayPath_Daily = outputpath + "MOD07_L2_RetrieveTa_"+year+'_'+ month_day +'_'+overpass+'_500hpa.tif'
    #                writeImageOut(DailyDomain_Array_500hpa_DayAverage, Layer500hpaDayPath_Daily, dtype, geot,noData)
                MonthDomain_Array_5hpa_DayDenominator[MonthDomain_Array_5hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_10hpa_DayDenominator[MonthDomain_Array_10hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_20hpa_DayDenominator[MonthDomain_Array_20hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_30hpa_DayDenominator[MonthDomain_Array_30hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_50hpa_DayDenominator[MonthDomain_Array_50hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_70hpa_DayDenominator[MonthDomain_Array_70hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_100hpa_DayDenominator[MonthDomain_Array_100hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_150hpa_DayDenominator[MonthDomain_Array_150hpa_DayDenominator==0]=np.nan
                
                MonthDomain_Array_200hpa_DayDenominator[MonthDomain_Array_200hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_250hpa_DayDenominator[MonthDomain_Array_250hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_300hpa_DayDenominator[MonthDomain_Array_300hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_400hpa_DayDenominator[MonthDomain_Array_400hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_500hpa_DayDenominator[MonthDomain_Array_500hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_620hpa_DayDenominator[MonthDomain_Array_620hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_700hpa_DayDenominator[MonthDomain_Array_700hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_780hpa_DayDenominator[MonthDomain_Array_780hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_850hpa_DayDenominator[MonthDomain_Array_850hpa_DayDenominator==0]=np.nan
                MonthDomain_Array_920hpa_DayDenominator[MonthDomain_Array_920hpa_DayDenominator==0]=np.nan
                
                ###****####
                MonthDomain_Array_5hpa_DayAverage=MonthDomain_Array_5hpa_Day/MonthDomain_Array_5hpa_DayDenominator
                MonthDomain_Array_10hpa_DayAverage=MonthDomain_Array_10hpa_Day/MonthDomain_Array_10hpa_DayDenominator
                MonthDomain_Array_20hpa_DayAverage=MonthDomain_Array_20hpa_Day/MonthDomain_Array_20hpa_DayDenominator
                MonthDomain_Array_30hpa_DayAverage=MonthDomain_Array_30hpa_Day/MonthDomain_Array_30hpa_DayDenominator
                MonthDomain_Array_50hpa_DayAverage=MonthDomain_Array_50hpa_Day/MonthDomain_Array_50hpa_DayDenominator
                MonthDomain_Array_70hpa_DayAverage=MonthDomain_Array_70hpa_Day/MonthDomain_Array_70hpa_DayDenominator
                MonthDomain_Array_100hpa_DayAverage=MonthDomain_Array_100hpa_Day/MonthDomain_Array_100hpa_DayDenominator
                MonthDomain_Array_150hpa_DayAverage=MonthDomain_Array_150hpa_Day/MonthDomain_Array_150hpa_DayDenominator
                
                MonthDomain_Array_200hpa_DayAverage=MonthDomain_Array_200hpa_Day/MonthDomain_Array_200hpa_DayDenominator
                MonthDomain_Array_250hpa_DayAverage=MonthDomain_Array_250hpa_Day/MonthDomain_Array_250hpa_DayDenominator
                MonthDomain_Array_300hpa_DayAverage=MonthDomain_Array_300hpa_Day/MonthDomain_Array_300hpa_DayDenominator
                MonthDomain_Array_400hpa_DayAverage=MonthDomain_Array_400hpa_Day/MonthDomain_Array_400hpa_DayDenominator
                MonthDomain_Array_500hpa_DayAverage=MonthDomain_Array_500hpa_Day/MonthDomain_Array_500hpa_DayDenominator
                MonthDomain_Array_620hpa_DayAverage=MonthDomain_Array_620hpa_Day/MonthDomain_Array_620hpa_DayDenominator
                MonthDomain_Array_700hpa_DayAverage=MonthDomain_Array_700hpa_Day/MonthDomain_Array_700hpa_DayDenominator
                MonthDomain_Array_780hpa_DayAverage=MonthDomain_Array_780hpa_Day/MonthDomain_Array_780hpa_DayDenominator
                MonthDomain_Array_850hpa_DayAverage=MonthDomain_Array_850hpa_Day/MonthDomain_Array_850hpa_DayDenominator
                MonthDomain_Array_920hpa_DayAverage=MonthDomain_Array_920hpa_Day/MonthDomain_Array_920hpa_DayDenominator
                
                noData = -32768
                pixel = Domain_GeoTransform[1]
                geot = Domain_GeoTransform
                dtype = gdal.GDT_Float32
                outputpath = r"D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge"
                
                Layer5hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_5hpa.tif'
                Layer10hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_10hpa.tif'
                Layer20hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_20hpa.tif'
                Layer30hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_30hpa.tif'
                Layer50hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_50hpa.tif'
                Layer70hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_70hpa.tif'
                Layer100hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_100hpa.tif'
                Layer150hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_150hpa.tif'
                
                Layer200hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_200hpa.tif'
                Layer250hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_250hpa.tif'
                Layer300hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_300hpa.tif'
                Layer400hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_400hpa.tif'
                Layer500hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_500hpa.tif'
                Layer620hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_620hpa.tif'
                Layer700hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_700hpa.tif'
                Layer780hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+ '_780hpa.tif'
                Layer850hpaDayPath = outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_850hpa.tif'
                Layer920hpaDayPath= outputpath + sensor +"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month) +'_'+overpass+'_920hpa.tif'
                
                ###*****####
                writeImageOut( MonthDomain_Array_5hpa_DayAverage, Layer5hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_10hpa_DayAverage, Layer10hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_20hpa_DayAverage, Layer20hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_30hpa_DayAverage, Layer30hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_50hpa_DayAverage, Layer50hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_70hpa_DayAverage, Layer70hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_100hpa_DayAverage, Layer100hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_150hpa_DayAverage, Layer150hpaDayPath, dtype, geot,noData)
                
                writeImageOut( MonthDomain_Array_200hpa_DayAverage, Layer200hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_250hpa_DayAverage, Layer250hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_300hpa_DayAverage, Layer300hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_400hpa_DayAverage, Layer400hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_500hpa_DayAverage, Layer500hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_620hpa_DayAverage, Layer620hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_700hpa_DayAverage, Layer700hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_780hpa_DayAverage, Layer780hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_850hpa_DayAverage, Layer850hpaDayPath, dtype, geot,noData)
                writeImageOut( MonthDomain_Array_920hpa_DayAverage, Layer920hpaDayPath, dtype, geot,noData)
     
                print("finished:"+sensor+"_L2_RetrieveTa_"+year+'_'+ "{:02d}".format(month))
    












