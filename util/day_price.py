# -*- coding: utf-8 -*-


from pandas import DataFrame, read_csv
import time,datetime
import pandas as pd #this is how I usually import pandas
from urllib import request
#from history import download
#http://table.finance.yahoo.com/table.csv?s=600000.ss    
#http://table.finance.yahoo.com/table.csv?s=000001.sz
# 分析当前股价,30日平均价,60日平均价,120日平均价,300日平均价,及差.
def anaPrice(save_url):
    datas = pd.read_csv(save_url,encoding="gbk",sep="\t")
    print(datas)
    current_close = 0 ;#当前收盘价.
    leiji_close = 0 ; # 累计收盘价之和
    avg_30 = 0;        # 30天收盘价平均价
    p_30 = 0;
    avg_60 = 0;        # 60天收盘价平均价
    p_60 = 0;
    avg_120 = 0;       # 120
    p_120 = 0;
    avg_300 = 0 ;      # 300.
    p_300 = 0;
    i = 0; #序号
    for index,row in datas.iterrows():
         val = row['Date,Open,High,Low,Close,Volume,Adj Close'].split(",");
         date = val[0];
         close = float(val[4]);
         vol = val[5];
         if (i ==0) :
             current_close = close;
         i  = i + 1;
         leiji_close = leiji_close + close;
         if (i == 30) :
             avg_30 = leiji_close / 30;
             p_30 = close;
         if (i == 60) :
             avg_60 = leiji_close /60 ;
             p_60 = close;
         if (i==120) :
             avg_120 = leiji_close /120;
             p_120 = close;
         if (i==300) :
             avg_300 = leiji_close /300;
             p_300 = close;
    
    print([current_close,avg_30,avg_60,avg_120,avg_300]);
    print([current_close,p_30,p_60,p_120,p_300]);
def download_now(load_url,save_url):
    webopen = request.urlopen(load_url)
    web_file = webopen.read()
    local_file = open(save_url,"wb")
    local_file.write(web_file)
    local_file.close()
    
    
code = "002004" #"600399";
load_url = "http://table.finance.yahoo.com/table.csv?s="+code+".sz "
save_url = "E:\\python\\F4838\\data\\daily\\"+code+".csv" 
print(load_url);
download_now(load_url,save_url)
anaPrice(save_url)

