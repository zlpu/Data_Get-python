import baostock as bs
import pandas as pd

"""
获取沪深A股历史日K线
"""
#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('登录状态码:'+lg.error_code)
print('登录信息:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
rs = bs.query_history_k_data_plus("sh.600941",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2020-01-01', end_date='2024-3-5',
    frequency="d", adjustflag="3")
print('历史K数据查询状态码:'+rs.error_code)
print('历史K数据查询信息:'+rs.error_msg)

# print(rs.get_row_data())

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
new_fields=["交易所行情日期","证券代码","开盘价","最高价","最低价","收盘价","前收盘价","成交量（累计 单位：股）","成交额（单位：人民币元）","复权状态(1：后复权， 2：前复权，3：不复权）",
            "换手率","交易状态(1：正常交易 0：停牌）","涨跌幅（百分比）","是否ST股，1是，0否"]
result = result.rename(columns=dict(zip(rs.fields, new_fields)))


#### 结果集输出到csv文件 ####
result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
print(result)

### 登出系统 ####
bs.logout()

