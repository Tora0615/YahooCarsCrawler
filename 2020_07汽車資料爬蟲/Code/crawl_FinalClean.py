# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:09:19 2020

@author: Arthur
"""
#軟體開發時間 Thu Jul  2 01:18:41 2020 ~ Tue Jul  7 20:09:23 2020

#https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/24?get_all=true 用這網址 & make_id 拿 model_id
#https://autos.yahoo.com.tw/v1/autos/newcar/trim/list/model/5906?get_all=true 用這網址 & model_id 拿 trim_id
#https://autos.yahoo.com.tw/cars-compare-result?trim_id={}%2C{}%2C{}%2C{} 用這網址 & trim_id 拿 詳細資料


from bs4 import BeautifulSoup  #使得html易看的套件
import requests  #向網站發送請求的套件
import json  #有時網站回傳的東西是json格式，用此套件可增加可讀性
import time  #設置延遲&計時用
import xlwt  #Excel寫入
import xlrd  #Excel讀取

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
            
            
#------------全部車子品牌的id (a~z 共52個)-------------
All_make_id = ["2","96","6","8","11","100","12","13","98","15","104","18","22","23","24","28","30","32","35","36","37","88","85","41","99","95","9","113","44","45","102","86","48","103","50","53","55","59","60","61","101","65","87","81","68","69","71","106","97","74","76","78"]
All_make_id_len =  len(All_make_id)
#----------------------------------------------------


#-------------- 用 make_id 取得 model_id 的函式--------------
def GetModelId(make_id_input):    
    while True:
        make_id = make_id_input
        url = 'https://autos.yahoo.com.tw/v1/autos/newcar/model/list/make/{}?get_all=true'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
        
       # ---------------暫時用不到-------------------
       # cookie 目前實測不用加
       # cookies = {'XSRF-TOKEN':'eyJpdiI6Im1ib2pGQXBIYndmQjZMZGQzNTFiTGc9PSIsInZhbHVlIjoiTk1DK0htNm04cXZEQlljTHF1OVdLSSt6N0VHZ290blNEZFNVaGR5alpNZDR4U3BRd0xjYWdGR093OUtFK2ZHciIsIm1hYyI6ImNmMWQ0NDJiZGZlNDRiMmFlNjFiOGFmMjk5ZGI3YjY4ZmMzMzUyZDUwMTUyZDdiZWFlOTM5ZGYwNjkzOWMzOWMifQ%3D%3D',
       #            'bc':'eyJpdiI6ImZGcE9wRXpvK1E4alJNcGViSTZ0K2c9PSIsInZhbHVlIjoiQXhHTWdOWDlWdUxEZEZYaG0wVGlzQjd2QWlKWlY3emxcL09RXC9sV0hkczlyT2Ntczh5N1BrZFdGY09qUGw0Y1duIiwibWFjIjoiZjIyMTcxNzk2Y2NhNjg5ZjhkZWVmZDZkMmY1MjQ1YjM5YzUzODcxNWYxN2IxNTk0NzFhMmRmNGFhMGY3NjkwNCJ9',
       #            'cmp':'t=1593707748&j=0',
       #            'laravel_session':'eyJpdiI6IjBUUVpNbklCTkdiUzJtVCtvWEpldWc9PSIsInZhbHVlIjoiTjgxRElKczJyazcrMXFUa0JRT2lcLzRMTVZpSnlXYXcwR0lsdGhtem4xZmRNSlh6WFhOZTd1bWxrSkhWZUVlUXgiLCJtYWMiOiI0ZmUwZjVmNmJjZDM5M2Y4OWU0NTlhM2E3YWJjODlhZTBhN2QzNDE2NDU5YWMyNjcxMzk4ZGJkMWY5NDAwZGQ1In0%3D'
       #            }
       # result = requests.get(url,cookies=cookies,headers=headers) #網址
       # ----------------------------------
        
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

        sheet1.write(col_count,0,All_make_id.index(str(trim_info_all['make_id']))+1) # 品牌ID(1~52) (make_id_count) (別人要求的) (52開始，不重複值加一)
        
        if(trim_info_all['make_cn_name'] == None): #踩雷:有些沒中文名稱
            sheet1.write(col_count,1,trim_info_all['make_en_name']) #品牌名稱(英)
        else:
            sheet1.write(col_count,1,trim_info_all['make_en_name']+'/'+trim_info_all['make_cn_name']) #品牌名稱(英+中) 
        
        sheet1.write(col_count,2,trim_info_all['model_year']) #年份
        sheet1.write(col_count,3,trim_info_all['model_name']) #型號名稱
        sheet1.write(col_count,4,model_id_count) # 型號ID(101~N) (model_id_count) (別人要求的) (101開始，不重複值加一)
        sheet1.write(col_count,5,(str)(trim_info_all['model_year'])+' '+trim_info_all['model_name']) #年份型號合併
        sheet1.write(col_count,6,trim_id_count) # 版本ID(5001~N) (trim_id_count) (別人要求的) (5001開始，不重複值加一)
        sheet1.write(col_count,7,trim_info_all['trim_name']) #版本名稱
        sheet1.write(col_count,8,trim_info_all['price']) #售價
        
        sheet1.write(col_count,40,trim_info_all['make_id']) # yahoo車廠id，記錄用
        sheet1.write(col_count,41,trim_info_all['model_id']) # yahoo車型id，記錄用
        sheet1.write(col_count,42,(str)(trim_info_all['trim_id'])) # yahoo版本id，記錄用
        
        while True:  #踩雷: 有時候 [Errno 13] Permission denied: 'car_test.xls'，可能是太頻繁存檔
            try:  #儲存成功:跳出 / 失敗:再試一次
                workbook.save('allcar_basic_info.xls') 
                break
            except:
                print('[Errno 13] Permission denied: \'car_test.xls\'')
                
        col_count += 1 #已經寫入數量加一
        trim_id_count +=1 #trim_id_count不會有重複，每次寫入數量就加一
        
    print('Get this model_id\'s All Trim Info. (model_id:'+str(all_model_id[i])+')')     
    print('↑',i+1,'/',len(all_model_id),';',format(float(i+1)/float(len(all_model_id))*100,'.2f'),'%')
    
    if (len(trim_info_json['autos']['result'][0]['trimlist'])!=0):  #踩雷:有些trim_info為0  #每次model_id所查詢的詳細資料數量，不等於0再加一
        model_id_count +=1 
        
    SleepFunction(col_count) # 每拿到trim_info就sleep
print('Get ALL TrimId & Basic Info Done. All Data have '+str(len(all_model_id)))
#-----------------------------

start_time = time.time() #GetSpec區塊計時用

#---------------------用 model_id 取得 技術規格 的函式--------------------
def GetSpec(id1,id2,id3,id4):  # From trim_id to get spec
    while True:
        url = 'https://autos.yahoo.com.tw/cars-compare-result?trim_id={}%2C{}%2C{}%2C{}'
        result = requests.get(url.format(id1,id2,id3,id4)) #填入值得網址
        soup = BeautifulSoup(result.text,'lxml') # result.text 讀入 BeautifulSoup / (result.text 為html內容)
        ul_all = soup.find("ul", {"class" :"spec" }).find_all("ul") #找到class為spec的ul，再找下一層'所有'ul
               
        temp=[]
        for i in range (len(ul_all)): #有幾個ul區塊，做幾次  #ul區塊是不同技術規格的分類
            li_all = ul_all[i].find_all("li")  #ul下的li區塊(有5個)  #li區塊是不同trim_id的查詢結果
            for j in range (len(li_all)):
                if(li_all[j].string == None): #看某車某規格是否存在
                    temp.append(' ') #若是空值，放入空白
                    continue
                tmpstr = (str)(li_all[j].string) #非空值，轉string，存入temp
                temp.append(tmpstr) #將值存入temp
         
        print('trim_id:'+ (str(id1)+','+str(id2)+','+str(id3)+','+str(id4))+' / Get Trim Id status '+ str(result.status_code))
        if (result.status_code == 200): #檢查html狀態碼(200是一切正常)
            return temp
        else:
            time.sleep(30)
#--------------------------------------------------------------------------       


#----------讀取先前的Excel-----------
data = xlrd.open_workbook('allcar_basic_info.xls')
table = data.sheet_by_name('工作表1') 
#-----------------------------------



#---------------若之前程式曾經中途結束過，則需要這段程式碼-------------------------
# 程式若結束過，就無法再用workbook.save，要改用new_excel.save
# 原理是: 讀舊Excel，複製一份到新的，再用新的當目標來操作，最後儲存

'''
from xlutils.copy import copy  #Excel copy 套件
old_excel = xlrd.open_workbook('allcar_basic_info.xls', formatting_info=True)   #開檔
new_excel = copy(old_excel)  # 將操作檔案物件拷貝，變成可寫的workbook物件   
sheet1 = new_excel.get_sheet(0)  # 獲得第一個sheet的物件  
'''
#-------------------------------------------------------------




#-------------GetSpec Main Code----------------
table_len = len(table.col_values(42))
GetSpecStart = time.time()
for i in range (1,table_len,4):   # 踩雷: out of range，所以多加了(table_len-i)的判斷    
    #----------trim_id 分配給 abcd-----------
    while True:
        if(i>table_len-4): #51  #接近結尾看擠個查幾個
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
        else: #平常四個一起查
            a = (str)((int)(table.col_values(42)[i]))
            b = (str)((int)(table.col_values(42)[i+1]))
            c = (str)((int)(table.col_values(42)[i+2]))
            d = (str)((int)(table.col_values(42)[i+3]))
            break
    #------------------------------------------
    
    
    
    #-------------資料抓取-------------
    tmp_arr = GetSpec(a,b,c,d) # 取得詳細技術規格的資料，存到arr裡
    #---------------------------------
    
    
    
    #----------看進度到哪裡------------
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
    #踩雷，如9382電動車會出問題，其技術規格標題與大部分有很多不同(油電混和車也是)        
    #為什麼用(i+k)，因為若: i = 0,4,8... , k = 0,1,2,3 , i+k = 0,1,2,3,4...     
            
    for k in range(4):  #四台車
        ArrID = 'car'+(str)(k+1) #car1~car4
        if(len(eval(ArrID+'[0]'))==1 and len(eval(ArrID+'[1]'))==1 and len(eval(ArrID+'[2]'))==1):  #抓回來都空值舊continue
            continue
        
        pos_fix_val = 0 #切輪胎尺寸後要用到的修正值
        for ii in range(len(tag)): #第一個tag~end
            for j in range (25):     #每個Excel tag 來比對
                if (tag[ii] in table.col_values(9+j+pos_fix_val)[0]):
                    if(tag[ii]=='輪胎尺碼'):  #對輪胎尺碼試著進行切割(切割依據:空白)
                        split_length = len(eval(ArrID+'['+str(ii)+']').split(' ')) #看切割長度   #踩雷:還有切割依據是逗號的，由於不多，最後手動處理                
                        if (split_length==2):  #切割成兩個
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[0])  #寫入第一個值
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[1])  #寫入第二個值
                        elif(split_length==3):  #踩雷:除了長度1、2，還有長度3的...(空格不小心空到兩格)     
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[0])  #有成功切割成兩個，寫入第一個值
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']').split(' ')[2])  #有成功切割成兩個，寫入第二個值
                        else:   #沒有切割，寫入同一個值
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']')) 
                            pos_fix_val=1
                            sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']'))
                    else:
                        sheet1.write(i+k,9+j+pos_fix_val,eval(ArrID+'['+str(ii)+']'))
                    break #減少無謂比較
                    
                else:
                    continue
            
               
        while True:
            try:
                new_excel.save('allcar_all_info.xls') 
                #workbook.save('allcar_basic_info')  #若要一次跑完用這個；若程式曾中斷，用上面的，這個要註解掉
                break
            except:
                print('[Errno 13] Permission denied: \'allcar_all_info.xls\', tring again')
                time.sleep(0.1)
        
       
        
    SleepFunction(i)  
    
    cost_time = time.time()-GetSpecStart  #迴圈至今花費總時間
    guess_remain = (cost_time/i)*table_len-cost_time  #預測剩餘時間  ((一則平均時間*資料全長)-已花時間)
    print('↑ 目前總花費時間: ',int(cost_time/(60*60)),'小時',int((cost_time-(60*60)*int(cost_time/(60*60)))/60),'分',int(cost_time%60),'秒'\
          ' / 預計剩餘時間: ',int(guess_remain/(60*60)),'小時',int((guess_remain-(60*60)*int(guess_remain/(60*60)))/60),'分',int(guess_remain%60),'秒\n')
    

end_time = time.time()        
total = end_time-start_time
print('總花費時間 : ',int(total/(60*60)),'小時',int((total-(60*60)*int(total/(60*60)))/60),'分',int(total%60),'秒') #時分秒
        













