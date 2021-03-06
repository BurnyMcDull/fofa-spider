import requests
import argparse
import base64
import re
from bs4 import BeautifulSoup
import time
import os
import threading
requests.packages.urllib3.disable_warnings()

def getTitle(url,filename,semlock):
    try:
        content = requests.get(url,timeout=1,verify=False)
        content.encoding='utf-8'
        pat = r'<title>(.*?)</title>'
        title = re.findall(pat,content.text)
        #print(title[0])
        try:
            filename.write(str(url)+','+str(title[0])+'\n')
        except:
            pass
        semlock.release()
    except :
        semlock.release()



if __name__ == '__main__':
    time_now=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    parser = argparse.ArgumentParser(description='fofa spider')
    parser.add_argument('-s', '--session', help='输入_fofapro_ars_session的值')
    parser.add_argument('-p','--page', help='输入爬取page的值',type=int,default=1)
    parser.add_argument('-t','--title', help='判断是否爬title',action="store_true")
    parser.add_argument('-w','--wait',default= 2 ,help='等待时间，默认2')
    parser.add_argument('-q','--fofa_sql',help='FOFA 查询语句')
    parser.add_argument('-n','--number',help='每页的结果数量,默认10条',type=int,default=50)
    parser.add_argument('-f','--file', help='输出文件地址,默认按照时间起名',default=time_now+'.csv')
    parser.add_argument('-m','--maxthread', help='爬取title的最大线程',type=int,default=50)
    given_args = parser.parse_args()
    page=given_args.page
    session = given_args.session
    sql=given_args.fofa_sql
    number=given_args.number
    filename=given_args.file
    threadMax = threading.BoundedSemaphore(int(given_args.maxthread))
    titleflag=given_args.title
    wait=given_args.wait
    bs_sql = base64.encodebytes(sql.encode('utf8')).decode()
    f=open(filename,'a')
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Accept':'*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'X-Requested-With':'XMLHttpRequest',
        'Cookie':  f'_fofapro_ars_session={session};result_per_page={number};'
    }

    for count in range(0,page):
        print(f'start:{count+1}')
        url1=f'https://fofa.so/result?page={int(count)}&qbase64={bs_sql}'
        response=requests.get(url1, headers=headers)
        response.encoding='utf-8'
        c=response.text.replace("$('#ajax_content').html(\"     \\n",'').replace('");\n// base.beautyScroll()','').replace('//$(\'.nicescroll-rails\').remove()','').replace('base.newBeautyScroll()','').replace('layui.form.render()','').replace('loadIconImage()','').replace('\\','')
        soup=BeautifulSoup(c,'html')
        if 'window.location.href=" /static_pages/error?' in response.text:
            print('爬虫停止，可能原因全部爬完或者session过期')
            break
        #print(soup)
        ip=soup.find_all('a',attrs={'target': '_blank'},href = True)
        for i in ip:
            url=i.attrs['href']
            if 'http' in url:
                f.write(f'{url}\n')
        time.sleep(int(wait))
    f.close()
    print('爬虫结束开始判断是否探测指纹')
    if(titleflag):
        print('title 爬取开始')
        count=0
        g=open(filename,'r')
        g_read=g.readlines()
        x=open(f'{time_now}_title.csv','a')
        for i in g_read:
            count=count+1
            i=i.replace('\n','')
            print(str(count)+'/'+str(len(g_read))+'\r',end='')
            threadMax.acquire()
            t=threading.Thread(target=getTitle,args=(i,x,threadMax,))
            t.start()
    else:
        print('无爬取需求')

            
                