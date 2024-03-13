# -*- coding:utf-8 -*-
import time, datetime
from selenium import webdriver
import pymysql
import re
import requests
import os

"""
标题：获取boss招聘网上的招聘全面数据(昆明)
目标站点分析：
(1) 目标url:固定地址+地区id+岗位名称+页数
(2) 反爬机制：目标站点虽然不用登陆也可以看到岗位信息,但是使用了动态的且时效不定的cookie,
所以很难使用requests(url,headers)+BeautifulSoup的方式获取数据
需要使用selenium的webdriver模拟浏览器的行为，注意每个页面打开的时间间隔，频率过快会导致ip封堵，如果有代理ip可以将ip添加到浏览器的代理中
方式：webdriver.Chrome.get(url)
(3) 网页结构分析：确定每个需求数据在html中的位置，
(4) 数据的获取：通过find_elements_by_class_name方法获取html中每个elements对象的标签数据
(5) 数据存储：pymysql，注意你的数据库中的表需要先创建好
create database if not exists zhaopin_db character set utf8 collate utf8_bin;
grant all privileges on zhaopin_db.* to python@'%' identified by ''python';
use zhaopin_db;\n
create table if not exists IT_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Admin_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Operation_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Sales_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Desgin_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Finance_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists Realty_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
create table if not exists medical_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));
"""

'''1.定义常量'''
'''输入相关信息'''
print("提示：\n请先在你的数据库中创建好数据库zhaopin_db,及数据库里面的表。\nsql语句如下：\n")
print(
        "create database if not exists zhaopin_db character set utf8 collate utf8_bin; \n"
        "grant all privileges on zhaopin_db.* to python@'%' identified by ''python'; \n"
        "use zhaopin_db;\n"
        "create table if not exists IT_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Admin_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Operation_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Sales_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Desgin_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Finance_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists Realty_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        "create table if not exists medical_info (id int primary key auto_increment,update_date char(101),job_name char(11),job_sales char(11),company_name char(11),company_area char(11),company_people char(11),job_limit char(11),job_url char(101),job_desc char(255));\n"
        )
# mysql_ip = input("请输入数据库ip:")
# mysql_port = int(input("请输入数据库端口号："))
# mysql_user = input("请输入数据库用户：")
# mysql_user_password = input("请输入该用户的密码：")
# 定义请求头
headers = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
# 数据库的连接信息
host_info = pymysql.connect(
    host='47.102.153.91:',
    port=3306,
    user='python',
    password='python',
    database='zhaopin_db',
    charset='utf8'
)

'''2.定义函数'''
# 每个传递岗位名字参数，获取5页数据


def start_search(key):
    """
    1.浏览器属性定义
    """
    # 1.1 实例化一个浏览器的属性设置
    options = webdriver.ChromeOptions()
    # 1.2 设置浏览器代理取爬数据
    # proxy="41.221.158.186:31932"
    # options.add_argument("--proxy-server={0}".format(proxy))
    # 1.3 设置请求头信息
    options.add_argument(headers)

    """
    2.模拟浏览器操作，定位数据位置，对element对象进行匹配标签操作来获取数据
    分析url组成=固定地址+岗位名称+页数
    """
    # 每个岗位我们获取5页数据
    for page in range(1, 15):
        # 防止访问速度过快，设置一个休眠时间30s,每30秒请求一次
        time.sleep(30)
        # 地址组成结构+固定地址+页面变量
        url_IT = 'https://www.zhipin.com/c101290100/?query=' + key + '&page=' + str(
            page) + "&ka=page-" + str(page)
        # 实例化一个浏览器,并作设置
        chrom_driver1 = webdriver.Chrome(options=options)
        # 在浏览器中访问目标地址
        chrom_driver1.get(url=url_IT)
        # 隐式等待，等待浏览器中的数据加载完，避免数据不全
        chrom_driver1.implicitly_wait(10)
        '''
        检测网页是否正常,分析被禁止访问的页面的元素。获取code 403
        如果：获取403字符串的语句正常执行，说明ip被禁止访问了，需要睡眠20分钟以后再继续
        如果：获取403语句执行异常，说明没有出现提示页面，可以正常访问岗位清单页面,可以进行数据的获取
        '''
        try:
            check_list = chrom_driver1.find_elements_by_class_name('error-content')
            status_code = check_list[0].find_element_by_class_name('text h1').text
            if status_code == '403':
                print("ip暂时被封禁，等待20分钟!")
                time.sleep(1200)  # 睡眠20分钟
        except:
            # 网页加载完以后，先判断网页是否正常
            try:  # 检测是否有异常
                # 分析html语法，通过选择html中的定位来获取我们的目标数据位置，因为是选择多个位置，使用find_elements_by_class_name方法，获取到一个list类型的数据
                job_list = chrom_driver1.find_elements_by_class_name('job-primary')
                # 获取到的list数据保存的是每个job-primary的element对象
                # print(job_list)
                # 遍历list中的每个element对象，获取里面的关键数据,职位名称-公司名称-公司地址-公司规模-薪资范围-工作年限要求-
                for li in job_list:
                    # print(li)
                    # 获取职位名称，通过分析css数据得到，职位名称位置在class=job-name下的a标签中
                    job_name = li.find_element_by_class_name('job-name a').text
                    # 获取公司名称
                    company_name = li.find_element_by_class_name('name a').text
                    # 获取公司地址
                    company_area = li.find_element_by_class_name('job-area').text
                    # 获取公司规模
                    company_people_all = li.find_element_by_class_name('info-company p').text
                    people = re.findall('\d+', company_people_all)
                    print(company_people_all, people)
                    if len(people) == 1:  # 分析规律，找到当只有一个数据时 list长度为1，所以只需要获取一个数据
                        company_people = str(people[0]) + '人以上'
                    else:  # list长度为2，需要获取2个数据组合起来
                        company_people = str(people[0]) + '-' + str(people[1]) + '人'
                    # 获取薪资范围
                    job_sales = li.find_element_by_class_name('red').text
                    # 工作年限要求
                    job_limit = li.find_element_by_class_name('job-limit p').text
                    # 岗位url，先通过element对象找到数据位置,再从中获取herf关键字的值，即：投递的地址
                    job_url = li.find_element_by_class_name('job-name a').get_attribute('href')
                    # 岗位职责，从岗位介绍里面获取职责信息（候补）
                    # chrom_drvier2 = webdriver.Chrome(options=options)
                    # chrom_drvier2.get(job_url)
                    # chrom_drvier2.implicitly_wait(10)
                    # job_desc = chrom_drvier2.find_element_by_class_name('text').text
                    # chrom_drvier2.quit()
                    """ 数据存储 """
                    print(job_name, company_name, company_area, company_people, job_sales, job_limit, "\n" + job_url)
                    '''数据库信息 '''
                    # 2.创建游标
                    cursor = host_info.cursor()

                    # 3.定义sql（insert）
                    # 判断请求的职位方向
                    # 将对应职位方向的数据存入对应的表
                    if key in (['医美','医助','护士','运维', 'IT', '信息化', 'java', 'python', 'C语言', '网络工程师', '信息安全', '前端']):
                        sql01 = "INSERT into IT_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    elif key in (['人力资源', '行政']):
                        sql01 = "INSERT into Admin_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    elif key in (['销售实习','实习']):
                        sql01 = "INSERT into Sales_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"

                    elif key in (['会计','财务']):
                        sql01 = "INSERT into Finance_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"

                    elif key in (['医生']):
                        sql01 = "INSERT into Medical_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    elif key in (['设计']):
                        sql01 = "INSERT into Desgin_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    elif key in (['兼职']):
                        sql01 = "INSERT into jianzhi_info (update_date,job_name,job_sales,company_name,company_area,company_people,job_limit,job_url,job_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"

                    # 4.执行sql

                    cursor.execute(sql01,
                                   [update_time, job_name, job_sales, company_name, company_area, company_people,
                                    job_limit,
                                    job_url, 'job_desc暂时不显示'])
                    # 5.提交事务
                    host_info.commit()
                    # 6.关闭光标
                    cursor.close()
                # 获取每一页的数据，将浏览器关闭
                chrom_driver1.quit()
            except:
                print("运行异常!")


if __name__ == '__main__':
    '''开始执行函数'''
    # 将当前时间写入数据库相关字段中
    update_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H时%M分")
    print(update_time)  # 打印开始时间
    # 需要搜索的职位list，遍历每个岗位，每个岗位间隔100秒再搜索
    # key_ = ['运维', 'IT', '信息化', 'java', 'python', '网络工程师', '兼职','信息安全', '前端', '人力资源', '行政', '设计', '销售', '财务', '护士',
    #         '医生']
    key_ = ['医美','医助','护士']
    for key in (key_):
        if key in (['医美','医助','护士']):
            time.sleep(300)
            start_search(key)
        else:
            time.sleep(100)
            start_search(key)
    # 执行结束，关闭数据库连接
    host_info.close()
    update_time_end = datetime.datetime.now().strftime("%Y年%m月%d日 %H时%M分")
    print(update_time_end)  # 打印结束时间
