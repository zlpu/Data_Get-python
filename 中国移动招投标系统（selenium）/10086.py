# -*- coding:utf-8 -*-


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import re

chrome_options = Options()
chrome_options.add_argument("--headless")#无请求头
base_url = "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"

DICT_list=['云南省某单位智能化、安防系统采购项目','云南省某单位违停抓拍监控系统集成服务采购项目',
           '河南省某单位电子警察系统采购项目','北京市某单位互联网出入口收敛建设采购项目',
           '四川省某单位会商系统设备采购项目','宁夏某单位设备部分采购项目']
for i in range(0,len(DICT_list)):
    driver = webdriver.Chrome(options=chrome_options, service_args=['--load-images=no'])
    try:
        driver.get(base_url)
        WebDriverWait(driver, 10)
        driver.get(base_url)
        time.sleep(10)
        driver.find_element(By.ID,'search').click()
        time.sleep(10)
        search_title=driver.find_element(By.ID,'title').\
            send_keys(DICT_list[i])
        time.sleep(6)
        driver.find_element(By.ID,'search').click()
        time.sleep(6)
        title=driver.find_element(By.XPATH,'//*[@id="searchResult"]/table/tbody/tr[3]/td[3]/a').text
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="searchResult"]/table/tbody/tr[3]/td[3]/a').click()
        time.sleep(1)
        windows = driver.window_handles
        time.sleep(1)
        driver.switch_to.window(windows[1])
        time.sleep(1)
        shoumai_time=driver.find_element(By.XPATH,'//*[@id="mobanDiv"]/table/tbody/tr[4]/td/div[1]/span').text
        print("投标报名时间:"+shoumai_time[41:76])
        time.sleep(1)
        yingda_time = driver.find_element(By.XPATH,'//*[@id="mobanDiv"]/table/tbody/tr[5]/td/div[2]/span').text
        print("投标应答时间："+yingda_time[37:54])
        time.sleep(1)
        id= driver.find_element(By.XPATH,'/html/body/input[2]').get_attribute("value")
        link="https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="+str(id)
        print("挂网链接如下："+link)
        print("项目名称："+DICT_list[i])

        driver.close()
    except Exception as error:
        print(str(error))
        driver.close()
    time.sleep(20)