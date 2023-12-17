from flask import request
from flask import Flask
from flask import render_template

import json
import sqlite3

app = Flask(__name__)


@app.template_filter()
def minus(value, arg):
    return value - arg


@app.template_filter()
def plus(value, arg):
    return value + arg


@app.route('/index')
def home():
    # 连接数据库
    conn = sqlite3.connect('che168.db')
    cursor = conn.cursor()
    # 查询数据库中车的数量
    cursor.execute('SELECT COUNT(*) FROM che168')
    result = cursor.fetchone()[0]
    # 车辆级别的数量
    cursor.execute('SELECT COUNT(DISTINCT 车辆级别) FROM che168')
    level = cursor.fetchone()[0]
    # 品牌的数量
    cursor.execute('SELECT COUNT(DISTINCT 品牌) FROM che168')
    brand = cursor.fetchone()[0]
    # 城市的数量
    cursor.execute('SELECT COUNT(DISTINCT 城市) FROM che168')
    city = cursor.fetchone()[0]

    print("二手车数量:", result, "车辆级别:", level, "品牌:", brand, "城市:", city)
    # 关闭数据库连接
    conn.close()
    return render_template("index.html", vehicles=result, level=level, brand=brand, city=city)


@app.route('/car')
def car():
    datalist = []
    con = sqlite3.connect("che168.db")
    cur = con.cursor()
    sql = "select * from che168"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)

    page = int(request.args.get('page', 1))
    per_page = 50  # 每页显示数量

    # 计算偏移量
    offset = (page - 1) * per_page

    # 执行查询
    cur.execute(f"SELECT * FROM che168 LIMIT {per_page} OFFSET {offset}")
    data = cur.fetchall()

    # 获取总数据条数
    cur.execute("SELECT COUNT(*) FROM che168")
    total_count = cur.fetchone()[0]

    # 计算总页数
    total_pages = total_count // per_page + (1 if total_count % per_page > 0 else 0)

    # 关闭数据库连接
    cur.close()
    con.close()

    return render_template('car.html', cars=data, page=page, per_page=per_page, total_pages=total_pages)

    # return render_template('car.html',movies = datalist,paginate=paginate)
    # return render_template('car.html',cars = datalist)
    # return render_template('car.html')


@app.route('/level')
def level():
    level = []  # 车辆等级
    num = []  # 每一个等级对应的车辆数量
    con = sqlite3.connect("che168.db")
    cur = con.cursor()
    sql = "select 车辆级别, count(车辆级别) from che168 where 车辆级别 != 'None' group by 车辆级别"
    data = cur.execute(sql)
    for item in data:
        level.append(str(item[0]))
        num.append(item[1])
        print(level, num)

    cur.close()
    con.close()
    return render_template('level.html', level=level, num=num)


if __name__ == '__main__':
    app.run()
