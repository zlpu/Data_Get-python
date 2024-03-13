import time
import pymysql


#获取时间
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")




#连接mysql
def conn_mysql():
    conn=pymysql.connect(
        host="156.253.68.253",
        user="lin",
        password="linlin",
        # host="10.160.1.11",
        # user="cov",
        # password="cov",
        db="china_db",

    )
    cursor=conn.cursor()
    return conn,cursor

def close_conn_mysql(conn,cursor):
    cursor.close()
    conn.close()

def query(sql,*args):
    conn,cursor=conn_mysql()
    cursor.execute(sql,args)
    res=cursor.fetchall()
    close_conn_mysql(conn,cursor)
    return res

#填写查询语句-----l1
def get_l1_data():
    sql="select updatatime,confirm,heal,dead from china_Total"
    res=query(sql)
    return res

#填写查询语句-----l2
def get_l2_data():
    sql="select updatatime,nowConfirm from china_Total"
    res=query(sql)
    return res


#填写查询语句-----c1
def get_c1_data():
    sql="select children_name,total_nowConfirm from detail where updatatime=(select updatatime from detail order by updatatime desc limit 1) group by children_name"
    res=query(sql)
    return res

#填写查询语句-----r1
def get_r1_data():
    sql="select confirm,heal,dead,nowConfirm from china_Total where updatatime=(select updatatime from china_Total order by updatatime desc limit 1)"
    res=query(sql)
    return  res[0]

#填写查询语句-----r2
def get_r2_data():
    sql="select confirm_add,heal_add,dead_add,nowConfirm_add from china_Add where updatatime=(select updatatime from china_Add order by updatatime desc limit 1)"
    res=query(sql)
    return  res[0]


#填写查询语句-----r3
def get_r3_data():
    sql="select children_name,total_nowConfirm from (select children_name,total_nowConfirm from detail where updatatime=(select updatatime from detail order by updatatime desc limit 1)group by children_name)as a order by total_nowConfirm desc limit 8"
    res=query(sql)
    return res

if __name__ == '__main__':
    get_l1_data()
    get_l2_data()
    get_c1_data()
    get_r1_data()
    get_r2_data()
    get_r3_data()
