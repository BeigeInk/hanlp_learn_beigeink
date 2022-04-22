import requests
import json
from bs4 import BeautifulSoup

#文学ur:0-9
wx_url='https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=911,914&page='
#科技:0-30
kj_url="https://pacaio.match.qq.com/irs/rcd?cid=92&token=54424c1ebe77ea829a41040a3620d0e7&ext=tech&page="
#财经:0-30
cj_url="https://pacaio.match.qq.com/irs/rcd?cid=92&token=54424c1ebe77ea829a41040a3620d0e7&ext=finance&page="
#军事：0-20
js_url='https://pacaio.match.qq.com/irs/rcd?cid=92&token=54424c1ebe77ea829a41040a3620d0e7&ext=milite&page='
#娱乐:30
yl_url="https://pacaio.match.qq.com/irs/rcd?cid=92&token=54424c1ebe77ea829a41040a3620d0e7&ext=ent&page="
#历史:30
ls_url='https://pacaio.match.qq.com/irs/rcd?cid=92&token=54424c1ebe77ea829a41040a3620d0e7&ext=history&page='
for page in range(30):
    a=requests.get(ls_url+str(page))
    temp_json=json.loads(a.content)
    for i in temp_json['data']:
        title=i['title']
        vurl=i['vurl']
        temp_whole=requests.get(vurl)
        soup = BeautifulSoup(temp_whole.content, 'html.parser')
        #xpath='/html/body/div[3]/div[1]/div[1]/div[2]'
        whole_list=list()
        for j in soup.find_all(class_='one-p'):
            whole_list.append(j.text)
        #print(whole_list)
        with open('data/历史/'+title.replace(" ","_").replace("/",'_').replace("?",'_')+'.txt','w+',encoding='utf-8')as f:
            f.write('\n'.join(whole_list))