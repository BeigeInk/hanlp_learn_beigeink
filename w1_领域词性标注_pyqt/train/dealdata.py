import os
with open('tn_pos.txt','r',encoding='ANSI') as f:
    orig=f.read()
with open('newdiseaseNames.txt','r',encoding='ANSI') as f:
    whole_date=f.read()
print(whole_date)
with open('new_del.txt','w+',encoding='utf-8') as f:
    f.write(orig)
    for i in whole_date.split('\n'):
        if i !='' or i!=' ':
            f.write(i+'/nd \n')