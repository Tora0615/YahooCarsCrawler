# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 01:18:41 2020

@author: Arthur
"""



from bs4 import BeautifulSoup
import requests
import json
import time

#id1='9647'
#id2='2309'
#id3='15109'
#id4='12499'

#id相同會被過濾掉


#https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/24?get_all=true
#https://autos.yahoo.com.tw/v1/autos/newcar/trim/list/model/5906?get_all=true




def GetModelId(make_id_input):    # From make_id to get model_id 
    make_id = make_id_input
    url = 'https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/{}?get_all=true'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
               'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
    '''
    # cookie 目前實測不用加
    cookies = {'XSRF-TOKEN':'eyJpdiI6Im1ib2pGQXBIYndmQjZMZGQzNTFiTGc9PSIsInZhbHVlIjoiTk1DK0htNm04cXZEQlljTHF1OVdLSSt6N0VHZ290blNEZFNVaGR5alpNZDR4U3BRd0xjYWdGR093OUtFK2ZHciIsIm1hYyI6ImNmMWQ0NDJiZGZlNDRiMmFlNjFiOGFmMjk5ZGI3YjY4ZmMzMzUyZDUwMTUyZDdiZWFlOTM5ZGYwNjkzOWMzOWMifQ%3D%3D',
               'bc':'eyJpdiI6ImZGcE9wRXpvK1E4alJNcGViSTZ0K2c9PSIsInZhbHVlIjoiQXhHTWdOWDlWdUxEZEZYaG0wVGlzQjd2QWlKWlY3emxcL09RXC9sV0hkczlyT2Ntczh5N1BrZFdGY09qUGw0Y1duIiwibWFjIjoiZjIyMTcxNzk2Y2NhNjg5ZjhkZWVmZDZkMmY1MjQ1YjM5YzUzODcxNWYxN2IxNTk0NzFhMmRmNGFhMGY3NjkwNCJ9',
               'cmp':'t=1593707748&j=0',
               'laravel_session':'eyJpdiI6IjBUUVpNbklCTkdiUzJtVCtvWEpldWc9PSIsInZhbHVlIjoiTjgxRElKczJyazcrMXFUa0JRT2lcLzRMTVZpSnlXYXcwR0lsdGhtem4xZmRNSlh6WFhOZTd1bWxrSkhWZUVlUXgiLCJtYWMiOiI0ZmUwZjVmNmJjZDM5M2Y4OWU0NTlhM2E3YWJjODlhZTBhN2QzNDE2NDU5YWMyNjcxMzk4ZGJkMWY5NDAwZGQ1In0%3D'
               }
    result = requests.get(url,cookies=cookies,headers=headers) #網址
    '''
    
    result = requests.get(url.format(make_id),headers=headers)
    print(result.status_code)
    return result


model_info_json = json.loads(GetModelId('48').text)  
print('GetModelId Done')
length = len(model_info_json['autos']['result'][0]['modellist'])
temp_model = []
for i in range (length):
#    #print(model_info_json['autos']['result'][0]['modellist'][i])
    #print(model_info_json['autos']['result'][0]['modellist'][i]['model_id'])
    temp_model.append(model_info_json['autos']['result'][0]['modellist'][i]['model_id'])



def GetTrimId(model_id_input):    # From model_id to get trim_id 
    model_id = model_id_input
    url = 'https://autos.yahoo.com.tw/v1/autos/newcar/trim/list/model/{}?get_all=true'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
               'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
    result = requests.get(url.format(model_id),headers=headers)
    print(result.status_code)
    return result
 
#----------寫到新檔案-----------   
import xlwt
workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
sheet1 = workbook.add_sheet("工作表1")          #新建sheet

col_count = 0
for i in  range(len(temp_model)):
    trim_info_json = json.loads(GetTrimId(temp_model[i]).text) # = json.loads(result.text) 
    for j in range(len(trim_info_json['autos']['result'][0]['trimlist'])):
        trim_info_all = trim_info_json['autos']['result'][0]['trimlist'][j] #shorter

        sheet1.write(col_count,0,trim_info_all['make_cn_name']+'/'+trim_info_all['make_en_name'])
        sheet1.write(col_count,1,trim_info_all['model_year'])
        sheet1.write(col_count,2,trim_info_all['model_name'])
        sheet1.write(col_count,3,(str)(trim_info_all['model_year'])+' '+trim_info_all['model_name'])
        sheet1.write(col_count,4,trim_info_all['trim_name'])
        sheet1.write(col_count,5,trim_info_all['price'])
        sheet1.write(col_count,37,trim_info_all['make_id'])
        sheet1.write(col_count,38,trim_info_all['model_id'])
        sheet1.write(col_count,39,(str)(trim_info_all['trim_id']))
        workbook.save('car_full.xls') 
        time.sleep(0.3)
        if(col_count%5==0):
            time.sleep(1)
        if(col_count%16==0):
             time.sleep(5)
        if(col_count%51==0):
                time.sleep(10)
        col_count += 1

print('GetTrimId Done')



#---------------------技術規格查詢--------------------

def GetSpec(id1,id2,id3,id4):  # From trim_id to get spec
    url = 'https://autos.yahoo.com.tw/cars-compare-result?trim_id={}%2C{}%2C{}%2C{}'
    result = requests.get(url.format(id1,id2,id3,id4)) #網址
    print(result.status_code) #200

    #print(result.text) #html內容
    soup = BeautifulSoup(result.text,'lxml') # result.text 讀入 BeautifulSoup
    
    #soup.find("ul", {"class" :"spec" }).find('ul')
    
    ul_all = soup.find("ul", {"class" :"spec" }).find_all("ul") #找到class為spec的ul，再找下一層所有ul
    
        
    temp=[]
    for i in range (len(ul_all)): #有幾個ul區塊，做幾次
        li_all = ul_all[i].find_all("li")  #ul下的li區塊(有5個)
        for j in range (len(li_all)):
            if(li_all[j].string == None):
                temp.append(' ') #若是空值，放入空白
                continue
            tmpstr = (str)(li_all[j].string) #非空值，轉string，存入temp
            #print(tmpstr)
            temp.append(tmpstr)
    return temp 

       




import xlrd
data = xlrd.open_workbook('car_full.xls')
table = data.sheet_by_name('工作表1') 
for i in range (0,len(table.col_values(39)),4):
    a = (str)((int)(table.col_values(39)[i]))
    b = (str)((int)(table.col_values(39)[i+1]))
    c = (str)((int)(table.col_values(39)[i+2]))
    d = (str)((int)(table.col_values(39)[i+3]))
    try:
        arr = GetSpec(a,b,c,d) #詳細資料回傳測試
    except:
        try:
            arr = GetSpec(a,b,c,c)
        except:
            try:
                arr = GetSpec(a,b,b,b)
            except:
                arr = GetSpec(a,a,a,a)
                

    tag = [] #標題
    car1 = []
    car2 = []
    car3 = []
    car4 = []
    
    for ii in range (len(arr)):
        if(ii%5 == 0):
            tag.append(arr[ii])
        if(ii%5 == 1):
            car1.append(arr[ii])
        if(ii%5 == 2):
            car2.append(arr[ii])
        if(ii%5 == 3):
            car3.append(arr[ii])
        if(ii%5 == 4):
            car4.append(arr[ii])

    for k in range(4):  
        ArrID = 'car'+(str)(k+1)
        #sheet1.write(i+k,6,eval(ArrID+'[11]'))  # i = 0,4,8... , k = 0,1,2,3 , i+k = 0,1,2,3,4...
        	
        sheet1.write(i+k,7,eval(ArrID+'[11]')) #輪胎規格(前)
        sheet1.write(i+k,8,eval(ArrID+'[11]')) #輪胎規格(後)	
        sheet1.write(i+k,9,eval(ArrID+'[2]')) #CC數
        sheet1.write(i+k,10,eval(ArrID+'[3]'))  #原廠馬力	
        sheet1.write(i+k,11,eval(ArrID+'[4]')) #原廠扭力
        #無 #0~100加速
        sheet1.write(i+k,12,eval(ArrID+'[13]')) #車門數
        sheet1.write(i+k,13,eval(ArrID+'[14]')) #座位數
        #sheet1.write(i+k,14,eval(ArrID+'[26]')) #牌照稅
        sheet1.write(i+k,14,eval(ArrID+'['+(str)(len(tag)-2)+']')) #牌照稅
        #sheet1.write(i+k,15,eval(ArrID+'[27]')) #燃料稅	
        sheet1.write(i+k,15,eval(ArrID+'['+(str)(len(tag)-1)+']')) #燃料稅	
        sheet1.write(i+k,16,eval(ArrID+'[0]'))#動力型式
        #sheet1.write(i+k,17,eval(ArrID+'[25]')) #平均油耗
        sheet1.write(i+k,17,eval(ArrID+'['+(str)(len(tag)-3)+']')) #平均油耗
        sheet1.write(i+k,18,eval(ArrID+'[15]')) #車身長度(mm)
        sheet1.write(i+k,19,eval(ArrID+'[16]')) #車身寬度(mm)	
        sheet1.write(i+k,20,eval(ArrID+'[17]')) #車身高度(mm)
        #-------new--------
        sheet1.write(i+k,21,eval(ArrID+'[1]')) #引擎
        sheet1.write(i+k,22,eval(ArrID+'[5]'))#壓縮比
        sheet1.write(i+k,23,eval(ArrID+'[6]'))#驅動型式
        sheet1.write(i+k,24,eval(ArrID+'[7]'))#變速系統
        sheet1.write(i+k,25,eval(ArrID+'[8]'))#前輪懸吊
        sheet1.write(i+k,26,eval(ArrID+'[9]'))#後輪懸吊
        sheet1.write(i+k,27,eval(ArrID+'[10]'))#煞車型式
        sheet1.write(i+k,28,eval(ArrID+'[12]'))#車身型式
        sheet1.write(i+k,29,eval(ArrID+'[18]'))#車重
        sheet1.write(i+k,30,eval(ArrID+'[19]'))#軸距
        #sheet1.write(i+k,31,eval(ArrID+'[20]'))#標準行李箱容量
        #sheet1.write(i+k,32,eval(ArrID+'[21]'))#後座傾倒行李箱容量
        #sheet1.write(i+k,33,eval(ArrID+'[22]'))#油箱容量
        #sheet1.write(i+k,34,eval(ArrID+'[23]'))#市區油耗
        #sheet1.write(i+k,35,eval(ArrID+'[24]'))#高速油耗
        sheet1.write(i+k,34,eval(ArrID+'['+(str)(len(tag)-5)+']'))#市區油耗
        sheet1.write(i+k,35,eval(ArrID+'['+(str)(len(tag)-4)+']'))#高速油耗
        workbook.save('car_full.xls')
    time.sleep(0.3)
    if(i%5==0):
        time.sleep(1)
    if(i%16==0):
        time.sleep(5)
    if(i%51==0):
        time.sleep(10)    
        
        
        
        
'''
#--------trim_info_json---------

trim_info_all = trim_info_json['autos']['result'][0]['trimlist'][i] #short 

#車廠make_name
trim_info_all['make_cn_name']+'/'+trim_info_all['make_en_name']

#年份
trim_info_all['model_year']

#車系model_name (型號)
trim_info_all['model_name']

#合併
(str)(trim_info_all['model_year'])+' '+trim_info_all['model_name']

#車款trim_name (版本)
trim_info_all['trim_name']

#新車價格price 
trim_info_all['price']


#-------------id---------------

#make_id
trim_info_all['make_id']

#model_id
trim_info_all['model_id']

#trim_id
trim_info_all['trim_id']


workbook.save('car_full.xls')   #儲存 

#-----------car[]------------

#輪胎規格(前)	
car[11]

#輪胎規格(後)	
car[11]

#CC數	
car[2]

#原廠馬力	
car[3] 

#原廠扭力	
car[4] 

#0~100加速	
#無 

#車門數	
car[13] 

#座位數	
car[14] 

#牌照稅	
car[26] 

#燃料稅	
car[27] 

#動力型式	
car[0] 

#平均油耗	
car[25] 

#車身長度(mm)	
car[15] 

#車身寬度(mm)	
car[16] 

#車身高度(mm)
car[17] 

#-------new--------

#引擎
car[1]

#壓縮比
car[5]

#驅動型式
car[6]

#變速系統
car[7]

#前輪懸吊
car[8]

#後輪懸吊
car[9]

#煞車型式
car[10]

#車身型式
car[12]

#車重
car[18]

#軸距
car[19]

#標準行李箱容量
car[20]

#後座傾倒行李箱容量
car[21]

#油箱容量
car[22]

#市區油耗
car[23]

#高速油耗	
car[24]

'''















