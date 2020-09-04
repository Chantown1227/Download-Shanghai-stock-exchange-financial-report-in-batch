# -*- coding = utf-8 -*-
# @time:2020/9/2 11:34
# Author:唐成
# @File:词云模板.py
# @Software:PyCharm

import json
import requests
import re
import os
import random
import time
import datetime

try:
    os.mkdir('./output')
except:
    pass

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

Type='QUATER2' #获取的财报类型：QUATER1 QUATER2 QUATER3 YEARLY

begin = datetime.date(2020,8,1)
end = datetime.date(2020,9,1)
def get_pdf(stock_list):
    urldict={}
    for stock in stock_list:
        print(f'stock: {stock}')
        time.sleep(random.uniform(1, 3))
        for i in range((end - begin).days+1):
            searchDate=str(begin + datetime.timedelta(days=i))

            try:
                response=requests.get('http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?jsonCallBack=jsonpCallback97255&isPagination=true&productId='+str(stock)+'&keyWord=&securityType=0101%2C120100%2C020100%2C020200%2C120200&reportType2=DQBG&reportType='+Type+'&beginDate='+searchDate+'&endDate='+searchDate+'&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1599181065177',headers=headers)
            except:
                continue

            json_str =response.text[19:-1]
            # print(json_str)
            datasets = json.loads(json_str)
            dataset=datasets['pageHelp']['data']
            # print(datasets['pageHelp']['data'])
            for line in dataset:
                # print(line)
                # print(line['URL'])
                download_url = 'http://www.sse.com.cn/' + line['URL']
                # print(download_url)
                if re.search('半年度报告',line['TITLE'],re.S):
                    if re.search('摘要',line['TITLE'],re.S):###避免下载一些年报摘要等不需要的文件###
                        pass
                    else:
                        if re.search('ST',line['TITLE'],re.S):###下载前要将文件名中带*号的去掉，因为文件命名规则不能带*号，否则程序会中断###
                            filename=line['SECURITY_CODE']+'-ST'+line['TITLE']+searchDate+ '.pdf'
                            urldict[line['TITLE']]=download_url
                            print('已获取：',filename)
                        else:
                            filename = line['SECURITY_CODE'] + line['TITLE'] + searchDate + '.pdf'
                            urldict[line['TITLE']] = download_url
                            print('已获取：',filename)
        # print(urldict)
        for name in urldict:
            url = urldict[name]
            # print(url)
            response = requests.get(url, headers=headers)
            file = open('./output/' + name + ".pdf", 'wb')
            file.write(response.content)
            file.close()
            print(f'{name} 下载完成')

def main():
    stock_list = []
    with open('stock.csv') as f:
        for line in f:
            stock_list.append(line.strip())
    for i in range(0, len(stock_list), 10):
        sub_stock_list = stock_list[i:i + 10]
        get_pdf(sub_stock_list)

if __name__ == '__main__':
    main()

