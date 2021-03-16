# fofa-spider
fofa-spider

```
usage: main.py [-h] [-s SESSION] [-p PAGE] [-t] [-w WAIT] [-q FOFA_SQL] [-n NUMBER] [-f FILE] [-m MAXTHREAD]

fofa spider

optional arguments:
  -h, --help            show this help message and exit
  -s SESSION, --session SESSION
                        输入_fofapro_ars_session的值
  -p PAGE, --page PAGE  输入爬取page的值
  -t, --title           判断是否爬title
  -w WAIT, --wait WAIT  等待时间，默认2
  -q FOFA_SQL, --fofa_sql FOFA_SQL
                        FOFA 查询语句
  -n NUMBER, --number NUMBER
                        每页的结果数量,默认10条
  -f FILE, --file FILE  输出文件地址,默认按照时间起名
  -m MAXTHREAD, --maxthread MAXTHREAD
                        爬取title的最大线程
```

 session 需要自行抓包获取,依赖请自行添加。

写法支持python3.6的f-string特性。