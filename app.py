from flask import request
from flask import Flask
from flask import render_template

import sqlite3

app = Flask(__name__)


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
def movie():
    # datalist = []
    # con = sqlite3.connect("che168.db")
    # cur = con.cursor()
    # sql = "select * from che168"
    # data = cur.execute(sql)
    # for item in data :
    #     datalist.append(item)
    # cur.close()
    # con.close()
    #
    # # 当前页码，从第一页开始
    # page = int(request.args.get("page", 1))
    # # 每页的数量
    # per_page = int(request.args.get('per_page', 25))
    # paginate = data.paginate(page, per_page, error_out=False)
    #
    # # return render_template('car.html',movies = datalist,paginate=paginate)
    # return render_template('car.html',cars = datalist)
    return render_template('car.html')


if __name__ == '__main__':
    app.run()
