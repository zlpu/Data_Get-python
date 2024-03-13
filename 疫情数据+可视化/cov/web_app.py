# -*- coding:utf-8 -*-
from flask import Flask
from flask import render_template
import db_query
from flask import jsonify

app = Flask(__name__)


# 定义首页
@app.route('/')
def start_page():
    return render_template("main.html")


# 获取时间
@app.route('/time')
def get_time():
    return db_query.get_time()


# 接收utils.py中l1的数据
@app.route('/l1')
def get_l1_data():
    data = db_query.get_l1_data()
    day_1, confirm, heal, dead = [], [], [], []
    for a, b, c, d in data:
        day_1.append(a.strftime("%m-%d"))
        confirm.append(b)
        heal.append(c)
        dead.append(d)

    return jsonify({"day_1": day_1, "confirm": confirm, "heal": heal, "dead": dead})


# 接收utils.py中l2的数据
@app.route('/l2')
def get_l2_data():
    data = db_query.get_l2_data()
    day_1, nowconfirm = [], []
    for a, c in data:
        day_1.append(a.strftime("%m-%d"))
        nowconfirm.append(c)

    return jsonify({"day_1": day_1, "nowconfirm": nowconfirm})


# 接受utils.py的c1的数据
@app.route("/c1")
def get_c1_data():
    res = []
    for tup in db_query.get_c1_data():
        # print(tup[0], tup[1])
        res.append({"name": tup[0], "value": int(tup[1])})
    # print(res)
    return jsonify({"data": res})


# 接受utils.py的r1的数据
@app.route("/r1")
def get_r1_data():
    data = db_query.get_r1_data()
    return jsonify({"confirm": data[0], "heal": data[1], "dead": data[2], "nowConfirm": data[3]})


# 接受utils.py的r2的数据

@app.route("/r2")
def get_r2_data():
    data = db_query.get_r2_data()
    return jsonify({"confirm_add": data[0], "heal_add": data[1], "dead_add": data[2], "nowConfirm_add": data[3]})


# 接收utils.py中c3的数据
@app.route('/r3')
def get_r3_data():
    data = db_query.get_r3_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(v)

    return jsonify({'city': city, 'confirm': confirm})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5499)
