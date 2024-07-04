import glob
import json

#jsonpath = 'D:/Research/ScientificData/DownloadDoc/MOD07_China/'
jsonpath = 'C:\\Users\\Parrji\\Desktop\\MODIS07\\'

json_files = glob.glob(jsonpath + "*.json")
print(json_files)
json_files = sorted(json_files) 
print(json_files)
years = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
overpasses = ['Day','Night']

for year in years:
    print(year) #调式观察for循环
    
    for overpass in overpasses:
        print(overpass)
        
        #targetstr = 'MOD07_' + overpass+'_'+ year
        targetstr = 'MYD07_' + overpass+'_'+ year
        print(targetstr)
        
        txtpath = jsonpath + targetstr + '.txt'
        print(txtpath)
        
        txt = open(txtpath,mode="w",encoding="utf-8") 
        
        if ('Day_Night' == overpass):

            for jsonfile in json_files:
                if (overpass in jsonfile and year in jsonfile):
                    with open(jsonfile) as jsonf:
                        
                        jsonurl = json.load(jsonf)
                        
                        for key_x,value_y in jsonurl.items():
                            if key_x!='query':
                                url = "https://ladsweb.modaps.eosdis.nasa.gov" + value_y['url'] + '\n'
                                txt.write(url)
        else:
            index = 0
            for jsonfile in json_files:

                if (overpass in jsonfile and year in jsonfile and 'Day_Night' not in jsonfile):
                    with open(jsonfile) as jsonf:
                        
                        jsonurl = json.load(jsonf)
                        print(jsonurl)
                        
                        for key_x,value_y in jsonurl.items():#range(1521)
                            print(list(jsonurl.items())[0][1])
                            print(key_x)
                            print(value_y)
                            print(jsonurl.items()(0))
                            if key_x!='query':
                                index = index + 1
                                url = "https://ladsweb.modaps.eosdis.nasa.gov" + value_y['url'] + '\n'
                                txt.write(url)
            print(index)
        txt.close() 
        
        #lines = []
        with open(txtpath) as f:
            contents = f.readlines()
            type(contents)
            #print(sorted(contents))
        print(len(contents)) 
        print('***********')
        contents = list(set(contents))#Removing duplicate strings from a list in python [duplicate]
        print(len(contents)) 
        contents.sort(key=lambda str: int(str.split('/')[-2]))
        txtpath_sorted = jsonpath + targetstr + 'sorted.txt'    
        file = open(txtpath_sorted,"w")
        file.writelines(contents)
        file.close()           
        
        
#%%file difference between China and Tibet  
        
jsonpath_Tibet = 'C:\\Users\\Parrji\\Desktop\\MODIS07'
json_files_Tibet = glob.glob(jsonpath_Tibet + "*.json")  
json_files_Tibet = sorted(json_files_Tibet) 

jsonpath_China = 'C:\\Users\\Parrji\\Desktop\\MODIS07'
json_files_China = glob.glob(jsonpath_China + "*.json")  
json_files_China = sorted(json_files_China)

years = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
overpasses = ['Day','Night']

for year in years:
    print(year)
    for overpass in overpasses:
        print(overpass)
        
        targetstr = 'MOD07_' + overpass+'_'+ year
        #txtpath = jsonpath + targetstr + '.txt'
        
        #txt = open(txtpath,mode="w",encoding="utf-8") 
        #index = 0
        json_list_Tibet = []
        for jsonfile_Tibet in json_files_Tibet:
            if (overpass in jsonfile_Tibet and year in jsonfile_Tibet and 'Day_Night' not in jsonfile_Tibet):
                with open(jsonfile_Tibet) as jsonf_Tibet:
                    
                    jsonurl_Tibet = json.load(jsonf_Tibet)
                    
                    for key_x_Tibet,value_y_Tibet in jsonurl_Tibet.items():
                        if key_x_Tibet!='query':
                            #index = index + 1
                            url_Tibet = "https://ladsweb.modaps.eosdis.nasa.gov" + value_y_Tibet['url'] + '\n'
                            json_list_Tibet.append(url_Tibet)
        json_list_China = []
        for jsonfile_China in json_files_China:
            if (overpass in jsonfile_China and year in jsonfile_China and 'Day_Night' not in jsonfile_China):
                with open(jsonfile_China) as jsonf_China:
                    
                    jsonurl_China = json.load(jsonf_China)
                    
                    for key_x_China,value_y_China in jsonurl_China.items():
                        if key_x_China!='query':
                            #index = index + 1
                            url_China = "https://ladsweb.modaps.eosdis.nasa.gov" + value_y_China['url'] + '\n'
                            json_list_China.append(url_China)
                            
                            
        #print(json_list_China)
        #print(json_list_Tibet)
        
        json_set_Tibet = set(json_list_Tibet)
        json_set_China = set(json_list_China)#Removing duplicate strings from a list in python [duplicate]
        print(len(json_set_Tibet)) 
        print(len(json_set_China))
        json_dif = list(json_set_China-json_set_Tibet)
        
        json_dif.sort(key=lambda str: int(str.split('/')[-2]))
        txtpath_sorted = jsonpath_China + targetstr + 'difsorted.txt'    
        file = open(txtpath_sorted,"w")
        file.writelines(json_dif)
        file.close() 
        
                    
            


