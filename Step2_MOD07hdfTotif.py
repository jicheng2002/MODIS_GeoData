import glob
import os
from osgeo import gdal

os.environ['PROJ_LIB'] = r'D:\Conda\Lib\site-packages\osgeo\data\proj'

hdf_files = glob.glob(os.path.join('D:\A-GISFolder\PythonSpatialData\Class4\MOD07\HDF', '*.hdf'))
tifpath = r'D:\A-GISFolder\PythonSpatialData\Class4\MOD07\TIF'

# Function to extract date from HDF file name
def extract_date(hdffile):
    # Assuming the date is in the format AYYYYMMDD within the file name
    base_name = os.path.basename(hdffile)
    date_str = base_name.split('.')[1]  # Adjust based on actual file naming convention
    return date_str

for hdffile in hdf_files:
    print(hdffile)
    date_str = extract_date(hdffile)
    tifname = f"MOD07A_{date_str}.tiff"
    
    hdf = gdal.Open(hdffile, gdal.GA_ReadOnly)
    hdf_metadata = hdf.GetMetadata()
    hdf_Sub = hdf.GetSubDatasets()
    
    inputname_sf = hdf_Sub[8][0]  # Adjust if necessary based on required subdataset
    outputname_sf = os.path.join(tifpath, tifname)
    
    # GDAL Warp command to convert HDF subdataset to GeoTIFF
    os.system(f"gdalwarp -of GTIFF -geoloc -t_srs EPSG:4326 -tr 0.05 0.05 -r near {inputname_sf} {outputname_sf}")

