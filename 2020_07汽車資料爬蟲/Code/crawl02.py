# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:06:04 2020

@author: Arthur
"""


from bs4 import BeautifulSoup  #使得html易看的套件
import requests  #向網站發送請求的套件
import json  #有時網站回傳的東西是json格式，用此套件可增加可讀性
import time  #設置延遲


#---------爬蟲sleep函數-----------
def SleepFunction(inputvalue):
    time.sleep(0.3)
    if(inputvalue%5==0):
        time.sleep(1)
    if(inputvalue%16==0):
         time.sleep(5)
    if(inputvalue%51==0):
            time.sleep(10)
#-------------------------------
            
'''            
            
#------------全部車子品牌的id (a~z 共52個)-------------
All_make_id = ["2","96","6","8","11","100","12","13","98","15","104","18","22","23","24","28","30","32","35","36","37","88","85","41","99","95","9","113","44","45","102","86","48","103","50","53","55","59","60","61","101","65","87","81","68","69","71","106","97","74","76","78"]
All_make_id_len =  len(All_make_id)
#----------------------------------------------------


#https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/24?get_all=true 用這網址 & make_id 拿 model_id
#https://autos.yahoo.com.tw/v1/autos/newcar/trim/list/model/5906?get_all=true 用這網址 & model_id 拿 trim_id
#https://autos.yahoo.com.tw/cars-compare-result?trim_id={}%2C{}%2C{}%2C{} 用這網址 & trim_id 拿 詳細資料


#-------------- 用 make_id 取得 model_id 的函式--------------
def GetModelId(make_id_input):    
    while True:
        make_id = make_id_input
        url = 'https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/{}?get_all=true'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
        
        #---------------暫時用不到-------------------
        # cookie 目前實測不用加
        #cookies = {'XSRF-TOKEN':'eyJpdiI6Im1ib2pGQXBIYndmQjZMZGQzNTFiTGc9PSIsInZhbHVlIjoiTk1DK0htNm04cXZEQlljTHF1OVdLSSt6N0VHZ290blNEZFNVaGR5alpNZDR4U3BRd0xjYWdGR093OUtFK2ZHciIsIm1hYyI6ImNmMWQ0NDJiZGZlNDRiMmFlNjFiOGFmMjk5ZGI3YjY4ZmMzMzUyZDUwMTUyZDdiZWFlOTM5ZGYwNjkzOWMzOWMifQ%3D%3D',
        #           'bc':'eyJpdiI6ImZGcE9wRXpvK1E4alJNcGViSTZ0K2c9PSIsInZhbHVlIjoiQXhHTWdOWDlWdUxEZEZYaG0wVGlzQjd2QWlKWlY3emxcL09RXC9sV0hkczlyT2Ntczh5N1BrZFdGY09qUGw0Y1duIiwibWFjIjoiZjIyMTcxNzk2Y2NhNjg5ZjhkZWVmZDZkMmY1MjQ1YjM5YzUzODcxNWYxN2IxNTk0NzFhMmRmNGFhMGY3NjkwNCJ9',
        #           'cmp':'t=1593707748&j=0',
        #           'laravel_session':'eyJpdiI6IjBUUVpNbklCTkdiUzJtVCtvWEpldWc9PSIsInZhbHVlIjoiTjgxRElKczJyazcrMXFUa0JRT2lcLzRMTVZpSnlXYXcwR0lsdGhtem4xZmRNSlh6WFhOZTd1bWxrSkhWZUVlUXgiLCJtYWMiOiI0ZmUwZjVmNmJjZDM5M2Y4OWU0NTlhM2E3YWJjODlhZTBhN2QzNDE2NDU5YWMyNjcxMzk4ZGJkMWY5NDAwZGQ1In0%3D'
        #           }
        #result = requests.get(url,cookies=cookies,headers=headers) #網址
        #----------------------------------
        
        result = requests.get(url.format(make_id),headers=headers)
        print('make_id:'+ str(make_id)+' / Get Model Id status '+ str(result.status_code))
        if (result.status_code == 200):
            return result
        else:
            time.sleep(30)
#------------------------------------------------------------

#------GetModelID------
all_model_id = [] #'所有'廠牌內所有model_id會存在這
for j in range (All_make_id_len):    
    model_info_json = json.loads(GetModelId(All_make_id[j]).text)  #從makeid抓json下來
    print('↑',j+1,'/',All_make_id_len,';',format(float(j+1)/float(All_make_id_len)*100,'.2f'),'%')
    length = len(model_info_json['autos']['result'][0]['modellist'])
    #temp_model = [] #'這個'廠牌內所有model_id會存在這，由於會被洗掉所以移到外面去
    for i in range (length):
        all_model_id.append(model_info_json['autos']['result'][0]['modellist'][i]['model_id'])
    SleepFunction(j) #sleep    
print('GetAllModelId Done\n')
#-----------------------



#-------------- 用 model_id 取得 trim_id 的函式--------------
def GetTrimId(model_id_input):
    while True:
        model_id = model_id_input
        url = 'https://autos.yahoo.com.tw/v1/autos/newcar/trim/list/model/{}?get_all=true'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
        result = requests.get(url.format(model_id),headers=headers)
        print('model_id:'+ str(model_id)+' / Get Trim Id status '+ str(result.status_code))
        if (result.status_code == 200):
            return result
        else:
            time.sleep(30)
#------------------------------------------------------------
    

#----------開新的Excel-----------   
import xlwt
workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
sheet1 = workbook.add_sheet("工作表1")          #新建sheet
#-----------------------------


#-----------GetTrimId & 一些基本資料------------------
# 已經有所有model_id。一個model_id可查到所有 'trim_id' 以及 '廠牌基本數據' ，遍歷所有trim_data，取得基本資訊
col_count = 1 #Excel寫幾行的計數
model_id_count = 101
trim_id_count = 5001
for i in  range(len(all_model_id)):
    trim_info_json = json.loads(GetTrimId(all_model_id[i]).text)  # 等於 json.loads(result.text) 
    
    for j in range(len(trim_info_json['autos']['result'][0]['trimlist'])):
        trim_info_all = trim_info_json['autos']['result'][0]['trimlist'][j] #簡短用

        sheet1.write(col_count,0,All_make_id.index(str(trim_info_all['make_id']))+1) # 0 品牌ID (1~52)
        
        if(trim_info_all['make_cn_name'] == None): #踩雷:有些沒中文名稱
            sheet1.write(col_count,1,trim_info_all['make_en_name']) #品牌名稱(英)
        else:
            sheet1.write(col_count,1,trim_info_all['make_en_name']+'/'+trim_info_all['make_cn_name']) #品牌名稱(英+中) 
        
        sheet1.write(col_count,2,trim_info_all['model_year']) #年份
        sheet1.write(col_count,3,trim_info_all['model_name']) #型號名稱
        sheet1.write(col_count,4,model_id_count) # 4 型號ID (101~N) (model_id_count)
        sheet1.write(col_count,5,(str)(trim_info_all['model_year'])+' '+trim_info_all['model_name']) #年份型號合併
        sheet1.write(col_count,6,trim_id_count) # 6 版本ID (5001~N) (trim_id_count)
        sheet1.write(col_count,7,trim_info_all['trim_name']) #版本名稱
        sheet1.write(col_count,8,trim_info_all['price']) #售價
        
        
        
        sheet1.write(col_count,40,trim_info_all['make_id'])
        sheet1.write(col_count,41,trim_info_all['model_id'])
        sheet1.write(col_count,42,(str)(trim_info_all['trim_id']))
        
        while True:  #踩雷: 有時候 [Errno 13] Permission denied: 'car_test.xls'
            try:
                workbook.save('car_test.xls') 
                break
            except:
                print('[Errno 13] Permission denied: \'car_test.xls\'')
                
        col_count += 1
        trim_id_count +=1 
        
    print('Get this model_id\'s All Trim Info. (model_id:'+str(all_model_id[i])+')')     
    print('↑',i+1,'/',len(all_model_id),';',format(float(i+1)/float(len(all_model_id))*100,'.2f'),'%')
    
    if (len(trim_info_json['autos']['result'][0]['trimlist'])!=0):  #踩雷:有些trim_info為0
        model_id_count +=1 
        
    SleepFunction(col_count) # 每拿到trim_info就sleep
print('Get ALL TrimId & Basic Info Done. All Data have '+str(len(all_model_id)))
#-----------------------------

'''

#------------(捨棄)技術規格動態數量查詢--------------
#技術規格數量非定值，會在27~30間跳動，本想說若數值變動就增加一行放置標籤。但由於效率低且和下方爬蟲內容有關，因此捨棄
#pre_length = 0
#url = 'https://autos.yahoo.com.tw/cars-compare-result?trim_id={}'
#result = requests.get(url.format((str)(trim_info_all['trim_id'])))
#soup = BeautifulSoup(result.text,'lxml')
#new_length = len(ul_all = soup.find("ul", {"class" :"spec" }).find_all("ul"))
#if(pre_length!=new_length):
#    pre_length=new_length
#    col_count+=1
#--------------------------

start_time = time.time()

#---------------------用 model_id 取得 技術規格 的函式--------------------
def GetSpec(id1,id2,id3,id4):  # From trim_id to get spec
    while True:
        url = 'https://autos.yahoo.com.tw/cars-compare-result?trim_id={}%2C{}%2C{}%2C{}'
        result = requests.get(url.format(id1,id2,id3,id4)) #填入值得網址
        #print(result.status_code) #200
    
        
        soup = BeautifulSoup(result.text,'lxml') # result.text 讀入 BeautifulSoup / (result.text 為html內容)
        
        #soup.find("ul", {"class" :"spec" }).find('ul')  #找到class為spec的ul，再找下一層'第一個'ul 
        ul_all = soup.find("ul", {"class" :"spec" }).find_all("ul") #找到class為spec的ul，再找下一層'所有'ul
        
            
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
         
        print('trim_id:'+ (str(id1)+','+str(id2)+','+str(id3)+','+str(id4))+' / Get Trim Id status '+ str(result.status_code))
        if (result.status_code == 200):
            return temp
        else:
            time.sleep(30)
#--------------------------------------------------------------------------       



#----------讀取先前的Excel-----------
import xlrd
data = xlrd.open_workbook('allcar_basic_info.xls')
table = data.sheet_by_name('工作表1') 
#-----------------------------------





#----------若之前曾經中途結束過-----------
from xlutils.copy import copy
old_excel = xlrd.open_workbook('allcar_basic_info.xls', formatting_info=True)
new_excel = copy(old_excel)  # 將操作檔案物件拷貝，變成可寫的workbook物件
sheet1 = new_excel.get_sheet(0)  # 獲得第一個sheet的物件
#-----------------------------------




#-------------GetSpec Main Code----------------
table_len = len(table.col_values(42))
GetSpecStart = time.time()
for i in range (1,table_len,4):   # 踩雷 out of range，所以多加了(table_len-i)的判斷 #踩雷，如9382電動車會出問題

    
    #----------trim_id 分配給 abcd-----------
    
    while True:
        if(i>table_len-4): #51
            a = (str)((int)(table.col_values(42)[i]))  #由於查詢時相同的會被略過，因此給予前面已出現的值
            if ((table_len-i)==1):   #有a沒bcd
                b=a
                c=a
                d=a     
                break
            b = (str)((int)(table.col_values(42)[i+1]))
            if ((table_len-i)==2):   #有ab沒cd
                c=b
                d=b   
                break
            c = (str)((int)(table.col_values(42)[i+2]))
            if ((table_len-i)==3):   #有abc沒d
                d=c  
                break
            d = (str)((int)(table.col_values(42)[i+3]))
            break
        else: #
            a = (str)((int)(table.col_values(42)[i]))
            b = (str)((int)(table.col_values(42)[i+1]))
            c = (str)((int)(table.col_values(42)[i+2]))
            d = (str)((int)(table.col_values(42)[i+3]))
            break
    #------------------------------------------
    
    
    #-------------資料抓取-------------
    tmp_arr = GetSpec(a,b,c,d) # 取得詳細技術規格的資料，存到arr裡
    
    
    if(i+3 > table_len-1): 
        now=table_len-1
    else: 
        now=i+3
    percent = float(now)/float(table_len-1)*100
    print('↑',now,'/',table_len-1,';',format(percent,'.2f'),'%')
    #---------------------------------
    
    
    #----長度及新陣列設定-----
    arr_len = len(tmp_arr)
    tag = [] #標題
    car1 = []
    car2 = []
    car3 = []
    car4 = []
    #------------------------
    
    
    #---------------資料分開-----------------
    for ii in range (arr_len): #由於tmp_arr內容混雜，分別存到四台車及標籤的陣列
        if(ii%5 == 0):
            tag.append(tmp_arr[ii])
        if(ii%5 == 1):
            car1.append(tmp_arr[ii])
        if(ii%5 == 2):
            car2.append(tmp_arr[ii])
        if(ii%5 == 3):
            car3.append(tmp_arr[ii])
        if(ii%5 == 4):
            car4.append(tmp_arr[ii])
    #----------------------------------------
            



        
    #------------------四台車分別寫入Excel---------------------------
            
            
    for k in range(4):  
        ArrID = 'car'+(str)(k+1) #car1~car4
        if(len(eval(ArrID+'[0]'))==1 and len(eval(ArrID+'[1]'))==1 and len(eval(ArrID+'[2]'))==1):  #空值continue
            continue
        #sheet1.write(i+k,6,eval(ArrID+'[11]'))  # i = 0,4,8... , k = 0,1,2,3 , i+k = 0,1,2,3,4...
        	
        
        
        
        
        
        '''
        pos_fix_val = 0 #切輪胎尺寸後要用到的修正值
        j_fix_val = 0

        for j in range(len(car1)):
            print(tag[j],table.col_values(9+j+pos_fix_val-j_fix_val)[0],tag[j] in table.col_values(9+j+pos_fix_val-j_fix_val)[0])
            print(j,9+j+pos_fix_val-j_fix_val)
            if (tag[j] in table.col_values(9+j+pos_fix_val-j_fix_val)[0]): # 讀標題key值，與tag值比對，符合就寫入，沒有就跳過
                
                if (j==11):   # j為11時，此時的資料是輪胎尺碼 / 當j經過11時，輪胎尺碼要一個當兩個用，所以要被寫入的資料格座標要往後移，此作法用fix_val來實現
                    if (len(eval(ArrID+'['+str(j)+']').split(' '))==2):  #對輪胎尺碼試著進行切割(切割依據:空白)；能切會變成2個，不能的話只有一個
                        sheet1.write(i+k,9+j+pos_fix_val-j_fix_val,eval(ArrID+'['+str(j)+']').split(' ')[0])  #有成功切割成兩個，寫入第一個值
                        pos_fix_val=1
                        sheet1.write(i+k,9+j+pos_fix_val-j_fix_val,eval(ArrID+'['+str(j)+']').split(' ')[1])  #有成功切割成兩個，寫入第二個值
                    else:   #沒有成功切割，寫入同一個值
                        sheet1.write(i+k,9+j+pos_fix_val-j_fix_val+,eval(ArrID+'['+str(j)+']')) 
                        pos_fix_val=1
                        sheet1.write(i+k,9+j+pos_fix_val-j_fix_val,eval(ArrID+'['+str(j)+']'))
                else:
                    sheet1.write(i+k,9+j+pos_fix_val-j_fix_val+,eval(ArrID+'['+str(j)+']'))
            else:
                j_fix_val+=1
                continue
        '''
        
        
        true_count=0
        pos_fix_val = 0 #切輪胎尺寸後要用到的修正值
        #j_fix_val = 0
        for ii in range(len(tag)): #第一個tag~end
            for j in range (25):    #每個Excel tag 來比對
                #print(tag[ii],table.col_values(9+j+pos_fix_val)[0],tag[ii] in table.col_values(9+j+pos_fix_val)[0])
                #print(ii,9+j+pos_fix_val)
                if (tag[ii] in table.col_values(9+j+pos_fix_val)[0]):
                    if(tag[ii]=='輪胎尺碼'):
                    #if (ii==11):   # j為11時，此時的資料是輪胎尺碼 / 當j經過11時，輪胎尺碼要一個當兩個用，所以要被寫入的資料格座標要往後移，此作法用fix_val來實現
                        split_length = len(eval(ArrID+'['+str(ii)+']').split(' '))
                        if (split_length==2):
                        #if (len(eval(ArrID+'['+str(ii)+']').split(' '))==2):  #對輪胎尺碼試著進行切割(切割依據:空白)；能切會變成2個，不能的話只有一個
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[0])  #有成功切割成兩個，寫入第一個值
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[1])  #有成功切割成兩個，寫入第二個值
                        elif(split_length==3):
                        #elif(len(eval(ArrID+'['+str(ii)+']').split(' '))==3):    #踩雷:空格偶爾有出現兩個的==                   #對輪胎尺碼試著進行切割(切割依據:空白)；能切會變成2個，不能的話只有一個
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[0])  #有成功切割成兩個，寫入第一個值
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[2])  #有成功切割成兩個，寫入第二個值
                        else:   #沒有成功切割，寫入同一個值
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']')) 
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']'))
                    else:
                        sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']'))
                    break
                    
                else:
                    continue
            
        
        #print(abc) #檢查用插斷點(有變數顯示)  
        
        
        
        while True:
            try:
                new_excel.save('allcar_all_info.xls') 
                break
            except:
                print('[Errno 13] Permission denied: \'allcar_all_info.xls\', tring again')
                time.sleep(0.1)
        
        #print(abc) #檢查用插斷點(有變數顯示)
        
    SleepFunction(i)  
    
    cost_time = time.time()-GetSpecStart  #迴圈至今花費時間
    guess_remain = (cost_time/i)*table_len-cost_time  #預測剩餘時間
    print('↑ 目前總花費時間: ',int(cost_time/(60*60)),'小時',int((cost_time-(60*60)*int(cost_time/(60*60)))/60),'分',int(cost_time%60),'秒'\
          ' / 預計剩餘時間: ',int(guess_remain/(60*60)),'小時',int((guess_remain-(60*60)*int(guess_remain/(60*60)))/60),'分',int(guess_remain%60),'秒\n')
    #print('預計剩餘時間: ',int(guess_remain/(60*60)),'小時',int((guess_remain-(60*60)*int(guess_remain/(60*60)))/60),'分',int(guess_remain%60),'秒')
    

end_time = time.time()        
total = end_time-start_time
print('總花費時間 : ',int(total/(60*60)),'小時',int((total-(60*60)*int(total/(60*60)))/60),'分',int(total%60),'秒') #時分秒
        










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















