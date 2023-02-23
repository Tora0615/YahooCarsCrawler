# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:28:53 2020

@author: Arthur
"""
'''
import time
count = 0

while True:
    try:
        while True:
            print(str(count))
            count+=1       
            if(count>1000):
                break
            time.sleep(1)
    except:  #status code error
        count-=1
        print('except'+str(count))  
        time.sleep(3)
    if(): #達成目的退出
        break

#--------------------------

    
def print4(a,b,c,d):
    return(str(a)+str(b)+str(c)+str(d))
    
def print3(a,b,c):
    d=0
    return print4(a,b,c,d)    
    
def print2(a,b):
    c=0
    return print3(a,b,c)    
    
def print1(a):
    b=0
    return print2(a,b)   
    
a=4
b=3
c=2
d=1
    
e = print4(a,b,c,d)
f = print3(a,b,c)  
g = print2(a,b)  
h = print1(a) 
    
print(e,f,g,h)
    

    
table_len = 10
for i in range (0,table_len,4):   # 踩雷 out of range，所以多加(table_len-i)

    print(i)
    if ((table_len-i)==1): 
        continue        
    print(i+1)
    if ((table_len-i)==2): 
        continue        
    print(i+2)
    if ((table_len-i)==3): 
        continue
    print(i+3)





import time
#start_time = time.time()  
#time.sleep(60)
#end_time = time.time()        
#print(end_time-start_time)

i = 1593974694.0980659 - 1593999999.0980659
#print(int(i/(60*60)),int((i-(60*60)*int(i/(60*60)))/60),int(i%60)) #時分秒
print('總花費時間 : ',int(i/(60*60)),'小時',int((i-(60*60)*int(i/(60*60)))/60),'分',int(i%60),'秒') #時分秒

cost = 60

percent = 10

guest = cost * 100 / percent

'''
true_count=0
pos_fix_val = 0 #切輪胎尺寸後要用到的修正值
#j_fix_val = 0
for ii in range(len(tag)): #第一個tag~end
    for j in range (25):    #每個Excel tag 來比對
        if (tag[ii] in table.col_values(9+j+pos_fix_val)[0]):
            true_count+=1
        print(tag[ii],table.col_values(9+j+pos_fix_val)[0],tag[ii] in table.col_values(9+j+pos_fix_val)[0])
        print(ii,9+j+pos_fix_val)
        if (j == 12):
            continue
        if (tag[ii] in table.col_values(9+j)[0]):
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
            continue
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            


