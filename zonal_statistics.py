# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:28:58 2023

@author: zhangwenjie
"""


import pandas as pd
from rasterstats import zonal_stats
shp_poly = r"E:\zonal_statistic\edge_guangyuan\guangyuan_shp\guangyuan.shp"
input_path = r"E:\zonal_statistic\guangyuan.tif"
df_out = pd.DataFrame()
stats = zonal_stats(shp_poly, input_path, stats=[ 'sum'])
df_out = pd.DataFrame.from_dict(data=stats)
df_out.to_csv(r'E:\zonal_statistic\try.csv', header=True, index_label='fid', encoding='gbk')
