"""爬取豆瓣网排行榜前十的电影"""
"""
说明：
1.豆瓣网站
https://movie.douban.com/chart
https://movie.douban.com/review/best/

soup1 = soup.find_all(width="75")  # 解析出电影名称
# print(soup1[0]['alt'])
soup2 = soup.find_all('span', class_="rating_nums")  # 解析出评分

list_name = []  列表
list_value = []  列表
dict_name_value = dict(zip(list_name, list_value))组合成字典
mv_top[i][0]#电影名
mv_top[i][1]#评分
"""

import requests
import time
from bs4 import BeautifulSoup
import pymysql

"""内容匹配及数据输出"""


def main_DBMV_top():
    # 1 爬取源
    url = "https://movie.douban.com/chart"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    # 2 发起http请求
    spond = requests.get(url, headers=header)
    res_text = spond.text
    # 3 内容解析
    soup = BeautifulSoup(res_text, "html.parser")
    soup1 = soup.find_all(width="75")  # 解析出电影名称
    soup2 = soup.find_all('span', class_="rating_nums")  # 解析出评分
    # 4数据的处理
    list_name = []  # 将电影名做成一个列表
    for i in range(10):
        list_name.append(soup1[i]['alt'])
    list_value = []  # 将评分值做成一个列表
    for i in range(10):
        list_value.append(soup2[i].text)

    dict_name_value = dict(zip(list_name, list_value))  # 将两个list转化为字典dict
    mv_top = sorted(dict_name_value.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 字典从大到小排序,type==list

    '''数据-->mysql---创建每日表'''
    conn = pymysql.connect(
        host='192.168.32.132',
        user='mv',
        password='mv',
        database='mv'
    );
    '''游标的使用----创建表，表名为top+当天日期'''
    cursor1 = conn.cursor()  # 获取游标
    sql1 = 'create table if not exists top' + str(
        update_time) + '(TOP int not null primary key AUTO_INCREMENT,update_time varchar(11),mv_name varchar(100),mv_values varchar(11)); '

    cursor1.execute(sql1)  # 执行语句
    conn.commit()
    cursor1.close()  # 释放游标
    conn.close()


    '''写入数据'''
    print("\033[1;31m豆瓣网电影评分TOP10:\033[0m")
    for i in range(len(mv_top)):
        mv_top_name = mv_top[i][0]  # 取出电影名,后期直接使用
        mv_top_value = mv_top[i][1]  # 取出评分，后期直接使用
        print("\033[1;32m第" + str(i + 1) + '名：' + str(mv_top_name) + ":" + str(mv_top_value) + "分\033[0m")
        conn2 = pymysql.connect(
            host='192.168.32.132',
            user='mv',
            password='mv',
            database='mv'
        );
        '''游标的使用----导入数据，第一列为自增列代表排名'''
        cursor2 = conn2.cursor()  # 获取游标
        sql2 = 'insert into top' + str(update_time) + ' (update_time,mv_name,mv_values) values (%s,%s,%s);'
        cursor2.execute(sql2, [update_time, mv_top_name, mv_top_value])  # 执行语句
        conn2.commit()
        cursor2.close()  # 释放游标
        conn2.close()


if __name__ == '__main__':
    update_time = time.strftime("%Y%m%d", time.localtime())  # 获取当天日期
    main_DBMV_top()  # 调用函数，抓取数据，传教mysql表，将数据写入nysql
    print('\033[0;31;46m表创建成功！\033[0m')
    print(update_time+"\033[0;31;46m的数据写入成功！！！\033[0m")
