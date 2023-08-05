import requests
from bs4 import BeautifulSoup
#########################
### editor  :   Li Jichen
### email   :   lijichen8c@163.com
#########################

class BaiduScaper():
    def __init__(self,whole : str,alters : list):
        self.__base = 'https://www.baidu.com'
        self.__my_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62"
            }
        self.__f = open(f'{whole}.tsv','w')
        self.__init_url = self.__gen_url(whole ,alters)
    def __gen_url(self,whole ,list_alters ):
        temp = ' | '.join(list_alters )
        return f'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=title: ( "{whole }" ({temp }))&tn=news'
    def __ruleout_none(self,tag_items):
        return 'None' if tag_items == None else tag_items.text
    def start(self):
        target_url = self.__init_url
        self.__f.write('\t'.join(('','news_title','media','time','\n')))
        line = 0
        while True:
            resp = requests.get(target_url,headers=self.__my_headers )
            bsout = BeautifulSoup(resp.text,'lxml')
            ans = bsout.find_all(name='div',attrs={'class':'result-op c-container xpath-log new-pmd'})
            if len(ans) == 0:
                self.__f.write('Things above is all!')
                break
            for _ in ans:
                title = _.find(name='h3').find('a').text
                scource = self.__ruleout_none(_.find('span',{'class':'c-color-gray c-font-normal c-gap-right'}))
                time = self.__ruleout_none(_.find('span',{'class':'c-color-gray2 c-font-normal'}))
                self.__f.write('\t'.join((str(line),title,scource,time,'\n')))
                line += 1
            if line >= 99:
                break
            asdlxsx_ssss3ds_da = bsout.find('a',{'class':'n'})
            if asdlxsx_ssss3ds_da == None:
                break
            target_url = self.__base + asdlxsx_ssss3ds_da['href']
        self.__f.close()


