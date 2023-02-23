# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 19:08:47 2021

@author: Arthur
"""

#2021/03/03 01:30 完成 / 總花費時間 :  0 小時 2 分 36 秒 / 共 310 筆資料

# header 中的 at-authorization : e1eba75272ae3ea4fa9e80459949feda4e63133a (必要)
# makeIdList : ['37','20','16','17','15','18','6','25','26','7','8','19','9','24','4','10','1','11','2','5','13','14','21','3']
# https://autos.yahoo.com.tw/v1/autos/newbike/trim/list/make/24 此網址 + makeid 拿回 trimid & model_id (modelid此處無用)
# https://autos.yahoo.com.tw/bike-search?make_id=24&trim_id=4265 此網址 + trimid 拿回 html data --> 還要點入，棄用
# https://autos.yahoo.com.tw/bikes-compare-result?trim_id={}%2C{}%2C{}%2C{}  直接以 trimid 比較四台技術規格

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
         time.sleep(2)
    if(inputvalue%51==0):
            time.sleep(5)


#------------全部摩托品牌的id (a~z 共24個)-------------
All_make_id = ['37','20','16','17','15','18','6','25','26','7','8','19','9','24','4','10','1','11','2','5','13','14','21','3']
#All_make_id = ["37","20"] #試抓用
All_make_id_len =  len(All_make_id)



#-------------- 用 make_id 取得 trim_id 的函式--------------
def GetTrimId(make_id_input):    
    while True:
        make_id = make_id_input
        url = 'https://autos.yahoo.com.tw/v1/autos/newbike/trim/list/make/{}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'at-authorization' : 'e1eba75272ae3ea4fa9e80459949feda4e63133a'} # auth 必要的
        result = requests.get(url.format(make_id),headers=headers)
        print('make_id:'+ str(make_id)+' / Get Trim Id status '+ str(result.status_code))
        if (result.status_code == 200):
            return result
        else:
            print('等待15秒...')
            time.sleep(15)
            print('再次嘗試中...')


#----------開新的Excel-----------   
workbook = xlwt.Workbook(encoding='utf-8')       #新建工作簿
sheet1 = workbook.add_sheet("工作表1")          #新建sheet
#-----------------------------




#------實際抓所有TrimID  && 寫入基本數據到Excel ------
all_trim_id = [] #'所有'廠牌內所有model_id會存在這
col_count = 1 #Excel寫幾行的計數
model_id_count = 10100
trim_id_count = 105001
past_model_id = ''

for j in range (All_make_id_len):    
    model_info_json = json.loads(GetTrimId(All_make_id[j]).text)  #從makeid抓json下來
    print('↑',j+1,'/',All_make_id_len,';',format(float(j+1)/float(All_make_id_len)*100,'.2f'),'%')
    length = len(model_info_json['autos']['result'][0]['trimlist'])
    for i in range (length):
        all_trim_id.append(model_info_json['autos']['result'][0]['trimlist'][i]['trim_id'])
        
        
        trim_info_all = model_info_json['autos']['result'][0]['trimlist'][i] #簡短用
        sheet1.write(col_count,0,All_make_id.index(str(trim_info_all['make_id']))+101) # 品牌ID(1~52) (make_id_count) (別人要求的) (52開始，不重複值加一)
        
        if(trim_info_all['make_cn_name'] == None): #踩雷:有些沒中文名稱
            sheet1.write(col_count,1,trim_info_all['make_en_name']) #品牌名稱(英)
        else:
            sheet1.write(col_count,1,trim_info_all['make_en_name']+'/'+trim_info_all['make_cn_name']) #品牌名稱(英+中) 
        
        sheet1.write(col_count,2,trim_info_all['model_year']) #年份
        sheet1.write(col_count,3,trim_info_all['model_name']) #型號名稱
        if(trim_info_all['model_id']!=past_model_id):
            past_model_id = trim_info_all['model_id']
            model_id_count += 1
        sheet1.write(col_count,4,model_id_count) # 型號ID(101~N) (model_id_count) (別人要求的) (101開始，不重複值加一)
        sheet1.write(col_count,5,(str)(trim_info_all['model_year'])+' '+trim_info_all['model_name']) #年份型號合併
        sheet1.write(col_count,6,trim_id_count) # 版本ID(5001~N) (trim_id_count) (別人要求的) (5001開始，不重複值加一)
        sheet1.write(col_count,7,trim_info_all['trim_name']) #版本名稱
        sheet1.write(col_count,8,trim_info_all['price']) #售價
        
        sheet1.write(col_count,40,trim_info_all['make_id']) # yahoo車廠id，記錄用
        #sheet1.write(col_count,41,trim_info_all['model_id']) # yahoo車型id，記錄用 --> 用不到
        sheet1.write(col_count,41,(str)(trim_info_all['trim_id'])) # yahoo版本id，記錄用
        
        while True:  #踩雷: 有時候 [Errno 13] Permission denied: 'car_test.xls'，可能是太頻繁存檔
            try:  #儲存成功:跳出 / 失敗:再試一次
                workbook.save('Motor_basic_info.xls') 
                break
            except:
                print('[Errno 13] Permission denied: \'Motor_basic_info.xls\'')
                
        col_count += 1 #已經寫入數量加一
        trim_id_count +=1 #trim_id_count不會有重複，每次寫入數量就加一
        
        
        
        
    SleepFunction(j) #sleep    
print('GetAllTrimId Done\n')


start_time = time.time() #GetSpec區塊計時用

#---------------------用 model_id 取得 技術規格 的函式--------------------
def GetSpec(id1,id2,id3,id4):  # From trim_id to get spec
    while True:
        url = 'https://autos.yahoo.com.tw/bikes-compare-result?trim_id={}%2C{}%2C{}%2C{}'
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


#----------讀取先前的Excel-----------
data = xlrd.open_workbook('Motor_basic_info.xls')
table = data.sheet_by_name('工作表1') 




sampleTag = ['動力型式','車身型式','引擎型式','排氣量','壓縮比','最大馬力','最大扭力','馬達出力','供油系統','變速型式','油箱容量','啟動方式','座高','車長','車寬','車高','車重','軸距','前輪尺碼','後輪尺碼','煞車型式','市區油耗','高速油耗','平均油耗','牌照稅','燃料費'] #標題
for j in range(len(sampleTag)):
     sheet1.write(0,j,sampleTag[j]) #年份


#-------------GetSpec Main Code----------------
table_len = len(table.col_values(41))
GetSpecStart = time.time()
for i in range (1,table_len,4):   # 踩雷: out of range，所以多加了(table_len-i)的判斷    
    #----------trim_id 分配給 abcd-----------
    while True:
        if(i>table_len-4): #51  #接近結尾看幾個查幾個
            a = (str)((int)(table.col_values(41)[i]))  #由於查詢時相同的會被略過，因此給予前面已出現的值
            if ((table_len-i)==1):   #有a沒bcd
                b=a
                c=a
                d=a     
                break
            b = (str)((int)(table.col_values(41)[i+1]))
            if ((table_len-i)==2):   #有ab沒cd
                c=b
                d=b   
                break
            c = (str)((int)(table.col_values(41)[i+2]))
            if ((table_len-i)==3):   #有abc沒d
                d=c  
                break
            d = (str)((int)(table.col_values(41)[i+3]))
            break
        else: #平常四個一起查
            a = (str)((int)(table.col_values(41)[i]))
            b = (str)((int)(table.col_values(41)[i+1]))
            c = (str)((int)(table.col_values(41)[i+2]))
            d = (str)((int)(table.col_values(41)[i+3]))
            break
    
    
    #-------------資料抓取-------------
    tmp_arr = GetSpec(a,b,c,d) # 取得詳細技術規格的資料，存到arr裡

    
    #----------看進度到哪裡------------
    if(i+3 > table_len-1): 
        now=table_len-1
    else: 
        now=i+3
    percent = float(now)/float(table_len-1)*100
    print('↑',now,'/',table_len-1,';',format(percent,'.2f'),'%')

    
    
    #----長度及新陣列設定-----
    tmp_arr_len = len(tmp_arr)
    
    tag = []
    car1 = []
    car2 = []
    car3 = []
    car4 = []
    
    #------------------------
    
    
    #---------------資料分開-----------------
    for ii in range (tmp_arr_len): #由於tmp_arr內容混雜，分別存到四台車及標籤的陣列
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
        
        tag_index_fix = 0
        for ii in range(len(tag)): #第一個tag~end
            try:
                sampleTag.index(tag[ii+tag_index_fix]) #以sample_tag來當作標題
                sheet1.write(i+k,9+sampleTag.index(tag[ii]),eval(ArrID+'['+str(ii)+']'))
            except:
                continue
                
            
               
        while True:
            try:
                #new_excel.save('allMoto_info.xls') 
                workbook.save('allMoto_info.xls')  #若要一次跑完用這個；若程式曾中斷，用上面的，這個要註解掉
                break
            except:
                print('[Errno 13] Permission denied: \'allMoto_info.xls\', tring again')
                time.sleep(0.1)
        
       
        
    SleepFunction(i)  
    
    cost_time = time.time()-GetSpecStart  #迴圈至今花費總時間
    guess_remain = (cost_time/i)*table_len-cost_time  #預測剩餘時間  ((一則平均時間*資料全長)-已花時間)
    print('↑ 目前總花費時間: ',int(cost_time/(60*60)),'小時',int((cost_time-(60*60)*int(cost_time/(60*60)))/60),'分',int(cost_time%60),'秒'\
          ' / 預計剩餘時間: ',int(guess_remain/(60*60)),'小時',int((guess_remain-(60*60)*int(guess_remain/(60*60)))/60),'分',int(guess_remain%60),'秒\n')
    

end_time = time.time()        
total = end_time-start_time
print('總花費時間 : ',int(total/(60*60)),'小時',int((total-(60*60)*int(total/(60*60)))/60),'分',int(total%60),'秒') #時分秒


















