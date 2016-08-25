# -*- coding: utf-8 -*-

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import os


import history

code = "sh600399";
codeList = [code]
load_url = "http://market.finance.sina.com.cn/downxls.php?date=#d#&symbol=#c#"
folder = "E:\\python\\F4838\\data\\#c#\\"
save_url = "E:\\python\\F4838\\data\\#c#\\#d#.csv"  
#downloads_daily(codeList,save_url,load_url,"2016-7-1","2016-7-22",folder)  


folder = "E:\\python\\F4838\\data\\all_temp\\"
#folder = "E:\\python\\F4838\\data\\"+code+"\\"
filelist = os.listdir(folder)
print(filelist)
print ("日期-00-00.csv","power"+"\t"+"成交量"+"\t"+"连续买入量"+"\t"+"连续卖出量"+"\t"+"小单差"+"\t"+"小单买入量"+"\t"+"四个点的价格"+"\t"+"小单比例")         



def calPower(file,folder):
    df = pd.read_csv(folder+file,encoding="gbk",sep="\t")
    #print (df.columns)
    #Index(['成交时间', '成交价', '价格变动', '成交量(手)', '成交额(元)', '性质'], dtype='object')
    power = 0
    small_bill_buy = 0;
    small_bill_sell = 0
    small_bill_cha = 0;
    p_index = 0;
    p_all_vol = 0;
    
    # 8个区间价格
    m_925=0
    m_1000 = 0
    m_1030 = 0
    m_1100 =0
    m_1130 =0
    m_1330 =0
    m_1400 =0
    m_1430 =0
    m_1500 =0
    
    # 连续买入变量 
    lianxu_buy = 0;
    lianxu_buy_vol = 0;
    lianxu_sell = 0;
    lianxu_sell_vol = 0;
    all_sell_vol = 0;
    all_buy_vol = 0;
    
    mf = 0;
    mf_buy =0
    mf_sell =0
    all_amount = 0;
    ic = 0; 
    ping_m = 0
    #  主动性买单和被东兴买单
    zhudong_buy = 0;
    beidong_buy = 0;
    if (df.size > 10):
        for index,row in df.iterrows():
            v_date = row['成交时间']
            open_date = v_date.split(":")[0]+v_date.split(":")[1]
            v_price = row['成交价']
            v_change = row['价格变动']
            if v_change == "--" :
                v_change = "0" 
            v_vol = row['成交量(手)']
            v_amount = row['成交额(元)']
            v_type = row['性质']
            
            p_all_vol += v_vol;
            #1-------------power--------------------
            this_power = float(v_change) * v_vol
            if open_date != "0925":
                power +=this_power
                
            if v_amount <= 40000 :
                if v_type == "买盘" :
                   small_bill_buy +=v_vol
                if v_type == "卖盘" :
                   small_bill_sell +=v_vol
                   
           #3------------总笔数--------------------
            p_index = p_index + 1
            #4-------------4个区价格
            cj_date = v_date.split(":")[0]+v_date.split(":")[1]+v_date.split(":")[2];
            #print(cj_date) 
            if open_date == "0925":
               m_925 = v_price
            if open_date == "1000":
                m_1000 = v_price
            if open_date == "1030":
                m_1030 = v_price
            if open_date == "1100":
                m_1100 = v_price
            if open_date == "1130":
                m_1130 = v_price
            if open_date == "1330":
                m_1330 = v_price
            if open_date == "1400":
                m_1400 = v_price
            if open_date == "1430":
                m_1430 = v_price
            if open_date == "1500":
                m_1500 = v_price
                
            #5 --连续买入
            if v_type == "买盘" :  
                lianxu_buy = lianxu_buy + 1
                lianxu_buy_vol += v_vol
                if (lianxu_sell >=5):
                    lianxu_sell = 0;
                    all_sell_vol += lianxu_sell_vol
                    lianxu_sell_vol  = 0
            if v_type == "卖盘" :
                lianxu_sell = lianxu_sell + 1
                lianxu_sell_vol += v_vol
                if (lianxu_buy >=5):
                    lianxu_buy = 0;
                    all_buy_vol += lianxu_buy_vol
                    lianxu_buy_vol = 0
            #6 ---mf，资金流净额:资金流金额。正表示流入、负表示流出 
            #7ic，资金流信息含量:abs（资金流净额/交易额）。ic>10%表明指标的信息含量较高。         
            #8mfp，资金流杠杆倍数:abs（流通市值/资金流净额）。用于衡量资金流的撬动效应。
            if float(v_change) > 0 :
                mf_buy += v_vol
                mf = mf + v_amount
            if float(v_change) < 0:
                mf_sell +=v_vol
                mf = mf - v_amount
            if float(v_change) == 0 :
                if v_type == "买盘" :
                   ping_m +=v_amount
                if v_type == "卖盘" :
                   ping_m -=v_amount
            #主被动买单
            if v_amount >= 400000 :
                if v_type == "买盘" :
                   zhudong_buy +=v_vol
                if v_type == "卖盘" :
                   beidong_buy +=v_vol
              
            all_amount += v_amount   
        small_bill_cha = small_bill_buy - small_bill_sell 
        if p_all_vol > 0:          
            small_rate = (small_bill_buy + small_bill_sell )/p_all_vol
        if all_amount > 0:
            ic = mf / all_amount;        
        
        #print (small_bill_cha)  
        #if power > 0 :\
        outputs = [];
        outputs.append(file)
        outputs.append(format(power,'.2f'))
        outputs.append(str(mf_buy-mf_sell));
        #outputs.append("总量:"+str(p_all_vol))
        tui_rate = format((mf_buy-mf_sell)/p_all_vol,'4f')
        outputs.append(""+str(tui_rate))#推动力量/总量
        outputs.append(""+str(format(mf/all_amount,'3f')))#资金主动额比:
        outputs.append(""+str(format(ping_m/all_amount,'3f')))#资金平价额比:
        dadan_rate = 0
        if beidong_buy == 0 :
            beidong_buy = 1;
        dadan_rate = zhudong_buy / beidong_buy;
        outputs.append(""+str(dadan_rate))#大单买卖量比:
        #$outputs.append("大单卖量:"+str(beidong_buy))
        outputs.append(""+str(small_bill_cha))#小单差:
        outputs.append("价格区间:["+str(m_925)+","+str(m_1000)+","+str(m_1030)+","+str(m_1100)+","+str(m_1130)+","+str(m_1330)+","+str(m_1400)+","+str(m_1430)+","+str(m_1500)+"]")
        outputs.append(""+str(all_amount))#总金额:
        #print(outputs)
       # print(file)
       # print("总量:"+str(p_all_vol)+";主动买量:"+str(zhudong_buy)+":主动卖量"+str(beidong_buy))
      #  print("总金额:"+str(all_amount)+";资金主动流额:"+str(mf)+";资金平价流额:"+str(ping_m))
        #if (mf_buy-mf_sell)>0 and mf >0 and ping_m >0:
        #print (file,format(power,'.2f') +"["+str(mf_buy-mf_sell)+"]"+"\t"+format(mf,'.2f')+format(ping_m,'.2f')+"\t"+format(ic,'.2f')+"\t"+ str(p_all_vol) +"\t"+str(all_buy_vol)+"\t"+str(all_sell_vol)+"\t"+ "\t"+ str(small_bill_cha) + "\t ["+str(m_925)+","+str(m_1000)+","+str(m_1030)+","+str(m_1100)+","+str(m_1130)+","+str(m_1330)+","+str(m_1400)+","+str(m_1430)+","+str(m_1500)+"]" +format(small_rate,'.2f')) 
        #if power>0 and float(tui_rate) > 0 and mf/all_amount > float(tui_rate) and dadan_rate > 0.58 and ping_m/all_amount > mf/all_amount:
        if (dadan_rate > 2):
            print(outputs)
              
         
for file in filelist: 
    calPower(file,folder)
    