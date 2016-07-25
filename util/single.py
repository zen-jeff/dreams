# -*- coding: utf-8 -*-

import history

codeList = ["sz002552"]
load_url = "http://market.finance.sina.com.cn/downxls.php?date=#d#&symbol=#c#"
folder = "E:\\python\\F4838\\data\\#c#\\"
save_url = "E:\\python\\F4838\\data\\#c#\\#d#.csv"  
downloads_daily(codeList,save_url,load_url,"2016-6-14","2016-7-13",folder) 