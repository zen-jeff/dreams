# -*- coding: utf-8 -*-


from urllib import request
#from history import download
#http://table.finance.yahoo.com/table.csv?s=600000.ss    
#http://table.finance.yahoo.com/table.csv?s=000001.sz

code = "603188";
load_url = "http://table.finance.yahoo.com/table.csv?s="+code+".ss "
save_url = "E:\\python\\F4838\\data\\daily\\"+code+".csv" 
download_now(load_url,save_url)

def download_now(load_url,save_url):
    webopen = request.urlopen(load_url)
    web_file = webopen.read()
    local_file = open(save_url,"wb")
    local_file.write(web_file)
    local_file.close()