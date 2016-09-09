# -*- coding: utf-8 -*-


# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv
import time,datetime
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import os
import history

folder = "E:\\python\\F4838\\data\\sh600399\\"
file = "E:\\python\\F4838\\data\\sh600399\\2016-07-21.csv"
code="600399";
daily_file = "E:\\python\\F4838\\data\\daily\\"+code+".csv";



#某天的收盘价
def day_price(d,file):
    
    datas = pd.read_csv(file,encoding="gbk",sep="\t")
    for index,row in datas.iterrows():
        val = row['Date,Open,High,Low,Close,Volume,Adj Close'].split(",");
        date = val[0];
        if (date ==d):
            return val[4];
#计算某个区间段的成交量情况.
def bo_daily(d,file):
    datas = pd.read_csv(file,encoding="gbk",sep="\t")
    bo_vol = 0 ; #波段期间总的量
    bo_every = 0; #波段期间平均量
    bo_nums = 0; #波段天数
    bo_begin = 0; #波段开始价格
    bo_end = 0; #波段结束价格
    for index,row in datas.iterrows():
        val = row['Date,Open,High,Low,Close,Volume,Adj Close'].split(",");
        date = val[0];
        close = val[4];
        vol = val[5];
        t = time.strptime(date, "%Y-%m-%d")
        before_t = time.strptime(d[0],'%Y-%m-%d');
        end_t = time.strptime(d[1],'%Y-%m-%d');
        if(before_t <= t and t <= end_t) :
            bo_vol += int(vol)
            bo_nums +=1
        if (before_t == t):
            bo_begin = float(val[2])
        if end_t == t :
            bo_end = float(close)
    bo_every = bo_vol /bo_nums /10000;
    cha = bo_end - bo_begin;
    print(d,str(bo_vol),str(bo_nums),str(format(bo_every,'.4f')),str(cha))


#计算分时图里的每个上升阶段，下跌阶段的成交量情况
def bo_in_day(d,file):
    datas = pd.read_csv(file,encoding="gbk",sep="\t")
    #某个日期的收盘价
    c =float( day_price(date,daily_file))
    
    if (datas.size > 10):
        gd = datas.groupby(['成交价','性质']).sum()
        small_close = 0;
        small_close_cha = 0
        big_close = 0;
        big_close_cha = 0
        for index,row in gd.iterrows():
            #如果分组价小于收盘价，
            if (index[0]<c):
                small_close = small_close +  int(row[0])
                
                if(index[1] == "买盘"):
                    small_close_cha = small_close_cha +  int(row[0])
                if(index[1] == "卖盘"):
                    small_close_cha = small_close_cha -int(row[0])
                    
            if (index[0] >=c):
                big_close = big_close +  int(row[0])
                
                if(index[1] == "买盘"):
                    big_close_cha = big_close_cha +  int(row[0])
                if(index[1] == "卖盘"):
                    big_close_cha = big_close_cha -int(row[0])
                
        print(c,small_close,small_close_cha,big_close,big_close_cha);
        if (datas.size > 10):
            bo_vol = 0;  # 波段成交量
            bo_buy_vol = 0; #波段主动买入量
            bo_sell_vol = 0; #波段主动卖出量.
            bo_nums = 0; #波段笔数.
            bo_every_vol = 0; #波段每笔交易数.
            for index,row in datas.iterrows():
                v_date = row['成交时间']
                
                v_price = row['成交价']
                v_change = row['价格变动']
                if v_change == "--" :
                    v_change = "0" 
                v_vol = row['成交量(手)']
                v_amount = row['成交额(元)']
                v_type = row['性质']
                cj_date = v_date.split(":")[0]+v_date.split(":")[1]+v_date.split(":")[2];
                
               
                fd = int(cj_date);
                if(fd>d[0] and fd<=d[1]):
                     # 波段成交量，笔数.
                    bo_vol += v_vol;
                    bo_nums += 1;
                    if v_type == "卖盘" or v_type == "中性盘":
                        bo_sell_vol += v_vol;
                    if v_type == "买盘" :
                        bo_buy_vol += v_vol
            bo_every_vol =format( bo_vol /bo_nums,'.2f')
            
            print(d,str(bo_vol)+"\t"+str(bo_nums)+"\t"+str(bo_every_vol)+"\t"+str(bo_buy_vol)+"\t"+str(bo_sell_vol))
     

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
        print(outputs)
#统计每笔的收益当天...总和.每笔和收盘价的差额就是盈亏俄.
def calMoney(sf,sfolder):
    df = pd.read_csv(sfolder+sf,encoding="gbk",sep="\t")
    win_money = 0
    if (df.size > 10):
        date = sf.split(".")[0];
        #if (date == "2016-07-27"):
            #close= 6.79
        #else:
        close = float(getClose("600399",date))
        #print(close,date)
        for index,row in df.iterrows():
            v_price = float(row['成交价'])
            v_vol = int(row['成交量(手)'])
            v_type = row['性质']
            win_money = win_money + (close -v_price) * v_vol *100
            #print(win_money)
        print(win_money)
        return win_money
#统计当天盈利的金额，当天亏损的金额，以及各自的成交量占比.
def calMoneyVol(sf,sfolder):
    df = pd.read_csv(sfolder+sf,encoding="gbk",sep="\t")
    win_money = 0
    win_vol = 0
    lose_money = 0
    lose_vol = 0
    if (df.size > 10):
        date = sf.split(".")[0];
        if (date == "2016-07-27"):
            close= 6.79
        else:
            close = float(getClose("600399",date))
        #print(close,date)
        for index,row in df.iterrows():
            v_price = float(row['成交价'])
            v_vol = int(row['成交量(手)'])
            v_type = row['性质']
            if (v_price <= close):
                win_money = win_money + (close -v_price) * v_vol *100
                win_vol += v_vol
            if (v_price > close) :
                lose_money = lose_money + (close -v_price) * v_vol *100
                lose_vol += v_vol
        if (lose_vol <= 0) :
            lose_vol = 1;
        print(win_money,lose_money,win_vol/lose_vol,win_vol,lose_vol)
        
#获取某天的收盘价.
def getClose(numcode,date):
    closeUrl = "E:\\python\\F4838\\data\\daily\\"+numcode+".csv" 
    return day_price(date,closeUrl);
    
date = "2015-12-30"



'''
多空双方的实力.
每季度的基金持股..
双汇发展,中航飞机.
'''
code = "sh600399";#"sh600797""sh600399",#
codeList = ["sh600399","sz000768","sh600685","sh601989","sh600418"];

load_url = "http://market.finance.sina.com.cn/downxls.php?date=#d#&symbol=#c#"
folder = "E:\\python\\F4838\\data\\#c#\\"
save_url = "E:\\python\\F4838\\data\\#c#\\#d#.csv"  

#1.下载
#downloads_daily(codeList,save_url,load_url,"2016-8-18","2016-8-23",folder)  


#sfolder = "E:\\python\\F4838\\data\\"+code+"\\"
#sfolder = "E:\\python\\F4838\\data\\all_temp\\"
#2.下载的文件列表
#filelist = os.listdir(sfolder)
#print(filelist)
#3.统计分析
for code in codeList:
    #1.下载
    downloads_daily([code],save_url,load_url,"2016-9-7","2016-9-9",folder)  
    
    sfolder = "E:\\python\\F4838\\data\\"+code+"\\"   
    
    filelist = os.listdir(sfolder)
    for sf in filelist:
        #bo_in_day([90000,155959],folder+sf)
        #print(sf)
        calPower(sf,sfolder)
        #当天盈亏总和.
        #win_money = calMoney(sf,sfolder)
        #calMoneyVol(sf,sfolder)
    

