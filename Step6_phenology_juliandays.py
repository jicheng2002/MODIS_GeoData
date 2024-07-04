#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 17:19:26 2021

@author: wenjiezhang
"""

#import time
import gdal
import numpy as np
from datetime import datetime, timedelta
#import pandas as pd
import glob,sys,os

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
    
MCD12Q2Path = '/Users/wenjiezhang/Research/Paper-Research/Phenology-Qinba/Result/MCD12Q2_Qinba_gdalwrap1000m/'
MCD12Q2Path = '/Users/wenjiezhang/Research/Paper-Research/Phenology-Qinba/Result/MCD12Q2_Qinba_gdalwrap500m/'


layers = ["Greenup","Dormancy"]
years = np.arange(2001,2018)

epoch = datetime.strptime('1970-01-01',"%Y-%m-%d" )


for layer in layers:
    print(layer)
    
    for year in years:
        
        MosaicTif = glob.glob(MCD12Q2Path + "MCD12Q2.A"+str(year)+ "."+layer+".tif")
        InputTif = MosaicTif[0]
        
        print(InputTif)
        subData = gdal.Open(InputTif)
        nodata = subData.GetRasterBand(1).GetNoDataValue()
        dtype = subData.GetRasterBand(1).DataType
        dtype = gdal.GetDataTypeName(dtype)
        geotransform = subData.GetGeoTransform()
        projection = subData.GetProjection()

        # number of bands
        bands = subData.RasterCount
        # ncols
        xsize = subData.RasterXSize
        # nrows
        ysize = subData.RasterYSize

        # get the array
        array = subData.ReadAsArray()
        rows = ysize
        cols = xsize
        for band in np.arange(2):
            print(band)
            band1_array = array[band,:,:]*1.0
            #print(band1_array)
            print(np.unique(array))
            band1_array[band1_array==32767] = np.nan
            
            junliandays = np.zeros((rows,cols))
            junliandays[junliandays==0] = np.nan
            
            for row in range(rows):
                for col in range(cols):
                    pixelvalue = band1_array[row,col]
                    if ~np.isnan(pixelvalue):
                        #print(pixelvalue)
                        #print([row,col])
                        onset_date = epoch+timedelta(pixelvalue)
                        julianday = onset_date.timetuple().tm_yday
                        junliandays[row,col] = julianday
                        
            outPath= "/Users/wenjiezhang/Research/Paper-Research/Phenology-Qinba/Result/MCD12Q2_Qinba_phenology1000m/"
            outPath= "/Users/wenjiezhang/Research/Paper-Research/Phenology-Qinba/Result/MCD12Q2_Qinba_phenology500m/"
            outPath_= outPath +"MCD12Q2.A"+str(year)+ "."+layer+"band"+str(band+1)+".tif"
            dtype = gdal.GDT_Float32
            writeImageOut(junliandays, outPath_, dtype, geotransform,nodata)
            

        
        
        
        
