import glob,sys,os
os.environ['PROJ_LIB'] = r'D:\Conda\Lib\site-packages\osgeo\data\proj'
from osgeo import gdal

#%%
def checkallgreater(list1, val):
    return(all(x > val for x in list1))

def checkallsmaller(list1, val):
    return(all(x < val for x in list1))

hdf_files = glob.glob(os.path.join('D:\GISFolder\PythonSpatialData\MODIS07\.idea' + '*.hdf'))
tifpath = r'D:\GISFolder\PythonSpatialData\PythonTest1\practice\2\tif'
for hdffile in hdf_files:
    print(hdffile)
    tifname = hdffile.split('\\')[-1].split('hdf')[0]+'.tiff'
    hdf = gdal.Open(hdffile, gdal.GA_ReadOnly)

    hdf_metadata = hdf.GetMetadata()
    hdf_Sub = hdf.GetSubDatasets()
    inputname_sf = hdf_Sub[8][0]
    outputname_sf = tifpath + '/' + tifname
    os.system('gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -te 73 25 105 41 -ts 1200 1200 -r bilinear ' + inputname_sf + ' ' + outputname_sf)