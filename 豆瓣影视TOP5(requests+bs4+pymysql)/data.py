"""爬取豆瓣网排行榜前十的电影"""

import requests
import time
from bs4 import BeautifulSoup


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

"""简单处理1，输入数值N，返回排第N的电影名及评分"""
# num=int(input("豆瓣网评分第N高的电影，N="))
# print(str(soup1[num-1]['alt'])+':'+soup2[num-1].text+'分')

"""处理2，将电影名和评分组成[{电影名：评分},{:}]的形式"""
list_name = []  # 将电影名做成一个列表
for i in range(5):
    list_name.append(soup1[i]['alt'])

list_value = []  # 将评分值做成一个列表
for i in range(5):
    list_value.append(soup2[i].text)

dict_name_value = dict(zip(list_name, list_value))  # 将两个list转化为字典dict
mv_top = sorted(dict_name_value.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 字典排序,type==list

print("\x1b[31m豆瓣电影评分TOP5 "+"\033[0m")
for i in range(len(mv_top)):
    mv_top_name = mv_top[i][0]  # 取出电影名,后期直接使用
    mv_top_value = mv_top[i][1]  # 取出评分，后期直接使用
    print("第" + "\x1b[31m"+str(i + 1) + '\033[0m' + "名：" + "\x1b[32m"+str(mv_top_name) + "\033[0m" + ":" + "\x1b[33m" + str(
        mv_top_value) + "\033[0m" + "分")
update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("刷新时间：" + str(update_time))

