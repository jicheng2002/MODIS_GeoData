# from osgeo import osr, gdal
# import numpy as np
# import os
# from PIL import Image
# import time
# from skimage import io
# import gdal
# def get_file_names(data_dir, file_type = ['tif','tiff']):
#     result_dir = [] 
#     result_name = []
#     for maindir, subdir, file_name_list in os.walk(data_dir):
#         for filename in file_name_list:
#             apath = maindir+'/'+filename
#             ext = apath.split('.')[-1]  
#             if ext in file_type:
#                 result_dir.append(apath)
#                 result_name.append(filename)
#             else:
#                 pass
#     return result_dir, result_name
        
# def get_same_img(img_dir, img_name):
#     result = {}
#     for idx, name in enumerate(img_name):
#         temp_name = ''       
#         for idx2, item in enumerate(name.split('_')[:-4]):
#             if idx2==0:
#                 temp_name = temp_name+item
#             else:
#                 temp_name = temp_name+'_'+item
    
#         if temp_name in result:
#             result[temp_name].append(img_dir[idx])
#         else:
#             result[temp_name] = []
#             result[temp_name].append(img_dir[idx])
#     return result  
          
# def assign_spatial_reference_byfile(src_path, dst_path):
#     src_ds = gdal.Open(src_path, gdal.GA_ReadOnly)
#     sr = osr.SpatialReference()
#     sr.ImportFromWkt(src_ds.GetProjectionRef())
#     geoTransform = src_ds.GetGeoTransform()
#     dst_ds = gdal.Open(dst_path, gdal.GA_Update)
#     dst_ds.SetProjection(sr.ExportToWkt())
#     dst_ds.SetGeoTransform(geoTransform)
#     dst_ds = None
#     src_ds = None
    
# def cut(in_dir, out_dir, file_type = ['tif','tiff'], out_type = 'png',out_size = 1024):
#     if not os.path.exists(out_dir):
#         os.makedirs(out_dir)
#     data_dir_list,_ = get_file_names(in_dir, file_type)    
#     count = 0
#     print('Cut begining for ', str(len(data_dir_list)), ' images.....' )
#     for each_dir in data_dir_list:
#         time_start = time.time()
#         #image = np.array(io.imread(each_dir))
#         image = np.array(Image.open(each_dir))
#         print(image.shape)
             
#         cut_factor_row = int(np.ceil(image.shape[0]/out_size))
#         cut_factor_clo = int(np.ceil(image.shape[1]/out_size))
#         for i in range(cut_factor_row):
#             for j in range(cut_factor_clo):
                
#                 if i == cut_factor_row-1:
#                     i = image.shape[0]/out_size-1
#                 else:
#                     pass
                
#                     if  j== cut_factor_clo-1:
#                             j = image.shape[1]/out_size-1
#                     else:
#                         pass
                        
#                 start_x = int(np.rint(i*out_size))
#                 start_y = int(np.rint(j*out_size))
#                 end_x = int(np.rint((i+1)*out_size))
#                 end_y = int(np.rint((j+1)*out_size)) 
        
                       
#                 temp_image = image[start_x:end_x,start_y:end_y,:]
 
#                 print('temp_image:',temp_image.shape)
#                 out_dir_images = out_dir+'/'+each_dir.split('/')[-1].split('.')[0] \
#                                +'_'+str(start_x)+'_'+str(end_x)+'_'+str(start_y)+'_'+str(end_y)+'.'+out_type
               
                
#                 out_image = Image.fromarray(temp_image)
#                 out_image.save(out_dir_images)
                
#                 src_path = r'D:\GISFolder\PythonSpatialData\PythonTest1\practice\2\tif\merge\A2023070.tif' #带地理影像
#                 assign_spatial_reference_byfile(src_path, out_dir_images)
    
                
#         count += 1
#         print('End of '+str(count)+'/'+str(len(data_dir_list))+'...')
#         time_end = time.time()
#         print('Time cost: ', time_end-time_start)
#     print('Cut Finsh!')
#     return 0
 
 
# def combine(data_dir, w, h, c, out_dir, out_type='tif', file_type=['tif', 'tiff']):
#     if not os.path.exists(out_dir):
#         os.makedirs(out_dir)    
#     img_dir, img_name = get_file_names(data_dir, file_type)
#     print('Combine begining for ', str(len(img_dir)), ' images.....' )
#     dir_dict = get_same_img(img_dir, img_name)                                                    
#     count = 0
#     for key in dir_dict.keys():
#         temp_label = np.zeros(shape=(w,h,c),dtype=np.uint8)
#         dir_list = dir_dict[key]
#         for item in dir_list:
#             name_split = item.split('_')
#             x_start = int(name_split[-4])
#             x_end = int(name_split[-3])
#             y_start = int(name_split[-2])
#             y_end = int(name_split[-1].split('.')[0])           
#             img = Image.open(item)
#             img = np.array(img)
#             temp_label[x_start:x_end,y_start:y_end,:]=img
            
            
#         img_name=key+'.'+out_type
#         new_out_dir=out_dir+'/'+img_name
            
#         label=Image.fromarray(temp_label)
#         label.save(new_out_dir)
#         src_path = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF\MOD07A_A2022335.tiff' #带地理坐标影像
#         assign_spatial_reference_byfile(src_path, new_out_dir)
#         count+=1
#         print('End of '+str(count)+'/'+str(len(dir_dict))+'...')
#     print('Combine Finsh!')
            
#     return 0  
    
# if __name__=='__main__':
#     ##### cut
#     # data_dir='F:/Level1'
#     # out_dir='F:/Level1/cut_960'
#     # file_type=['tif']
#     # out_type='tif'
#     # cut_size=960
       
#     # cut(data_dir,out_dir,file_type,out_type,cut_size)
#     ##### combine
#     data_dir=r'D:\GISFolder\PythonSpatialData\PythonTest1\practice\2\tif\merge'
#     h=3072
#     w=1792
#     c=3
#     out_dir=r'D:\GISFolder\PythonSpatialData\PythonTest1\practice\2\data'
#     out_type='tif'
#     file_type=['tif']
    
#     combine(data_dir, w, h, c, out_dir, out_type, file_type)



import glob, sys, os
from datetime import datetime, timedelta
import pandas as pd
from osgeo import gdal
import numpy as np
from osgeo import gdal_array
from pytz import timezone
from osgeo import gdal

def writeImageOut(outarray, outfile, dtype, gt, nodata):
    outarray[np.isnan(outarray)] = -32768
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    
    outDs = driver.Create(outfile, outarray.shape[2], outarray.shape[1], 20, dtype)
    if outDs is None:
        print('Could not create', outfile)
        sys.exit(1)
    for i, image in enumerate(outarray, 1):
        outDs.GetRasterBand(i).WriteArray(image)  
        outDs.GetRasterBand(i).SetNoDataValue(nodata)
    outDs.SetGeoTransform(gt)
    proj = '''GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137
    ,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433
    ,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'''
    outDs.SetProjection(proj)
    outDs.FlushCache() 
    outDs = None

def checkallgreater(list1, val):
    return all(x > val for x in list1)

def checkallsmaller(list1, val):
    return all(x < val for x in list1)

Nlat = 90
Slat = 0
Elon = 145
Wlon = 45
Empty_Arrary = np.zeros((20, 1800, 2000)) * np.nan
Empty_Arrary1 = np.zeros((20, 1800, 2000)) * np.nan
tip_file = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\TIF'
TifFile = glob.glob(tip_file + "*.tif")
i = 0

for file in TifFile:
    i += 1
    Tile_MOD07_RTP = gdal.Open(file)
    Tile_cols = Tile_MOD07_RTP.RasterXSize
    Tile_rows = Tile_MOD07_RTP.RasterYSize
    Tile_GeoTransform = Tile_MOD07_RTP.GetGeoTransform()
    Tile_MOD07_RTP_data = Tile_MOD07_RTP.ReadAsArray() / 1.0
    np.unique(Tile_MOD07_RTP_data)
    Tile_MOD07_RTP_data.shape
    np.nanmax(Tile_MOD07_RTP_data)

    xOffset = abs(int((45 - Tile_GeoTransform[0]) / 0.05))
    yOffset = abs(int((90 - Tile_GeoTransform[3]) / 0.05))
    
    if i > 1:
        Empty_Arrary1[0:20, yOffset:yOffset+Tile_MOD07_RTP_data.shape[1], xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = Tile_MOD07_RTP_data
        Empty_Arrary[np.isnan(Empty_Arrary)] = 0
        Empty_Arrary1[np.isnan(Empty_Arrary1)] = 0
        Empty_Arrary[np.where(Empty_Arrary < 0)] = 0
        Empty_Arrary1[np.where(Empty_Arrary1 < 0)] = 0
        Empty_ArraryA = Empty_Arrary + Empty_Arrary1
        np.unique(Empty_ArraryA)
        Empty_Arrary[np.where(Empty_Arrary > 0)] = 1
        Empty_Arrary1[np.where(Empty_Arrary1 > 0)] = 1
        Empty_ArraryB = Empty_Arrary + Empty_Arrary1
        Empty_ArraryB[Empty_ArraryB == 0] = np.nan
        Empty_Arrary = Empty_ArraryA / Empty_ArraryB
    else:
        Empty_Arrary[0:20, yOffset:yOffset+Tile_MOD07_RTP_data.shape[1], xOffset:xOffset+Tile_MOD07_RTP_data.shape[2]] = Tile_MOD07_RTP_data

np.unique(Empty_Arrary)
GeoTransform = (45.0, 0.05, 0.0, 90.0, 0.0, -0.05)
noData = -32768
dtype = gdal.GDT_Float32
tip_file_ = r'D:\A-GISFolder\PythonSpatialData\PythonTest1\practice\MOD07\Merge\merged_output.tif'

writeImageOut(Empty_Arrary, tip_file_, dtype, GeoTransform, noData)
