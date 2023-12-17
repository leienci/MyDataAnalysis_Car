from flask import request, send_file, jsonify
from flask import Flask
from flask import render_template
from wordcloud import WordCloud

import io
import sqlite3

app = Flask(__name__)


@app.template_filter()
def minus(value, arg):
    return value - arg


@app.template_filter()
def plus(value, arg):
    return value + arg


# 主页
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


# 二手车页面
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


# 车辆级别页面
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


# 城市页面
@app.route('/city')
def city():
    city = []  # 车辆等级
    num = []  # 每一个等级对应的车辆数量
    con = sqlite3.connect("che168.db")
    cur = con.cursor()
    # 查询每个城市的车辆数量
    sql = "select 城市, count(城市) from che168 where 城市 != 'None' group by 城市"
    data = cur.execute(sql)
    for item in data:
        city.append(str(item[0]))
        num.append(item[1])
        print(city, num)
    cur.close()
    con.close()
    return render_template('city.html', city=city, num=num)


# 生成品牌词云
@app.route('/wordcloud')
def wordcloud():
    # 连接数据库
    conn = sqlite3.connect('che168.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 品牌 FROM che168")
        results = cursor.fetchall()
        # 提取品牌名称列表
        brand_names = [result[0] for result in results]
        # 将品牌名称转换为字符串
        text = ' '.join(brand_names)
        # 设置中文字体路径
        font_path = './YouSheBiaoTiHei-2.ttf'
        # 创建词云对象，并指定字体路径
        wordcloud = WordCloud(width=1100, height=500, background_color='white', font_path=font_path).generate(text)
        # 生成词云图像
        image = wordcloud.to_image()
        # 将图像保存为字节流
        img_byte = io.BytesIO()
        image.save(img_byte, format='PNG')
        img_byte.seek(0)
        print('词云生成成功^_^')

        conn.close()
        # 返回词云图像
        return send_file(img_byte, mimetype='image/png')

    except Exception as e:
        conn.close()
        return str(e)


# 品牌词云页面
@app.route('/brand')
def bard():
    return render_template('brand.html')


# 变速箱页面
@app.route('/gearbox')
def gearbox():
    gearbox = []  # 车辆变速箱
    num = []  # 每一个等级对应的车辆数量
    con = sqlite3.connect("che168.db")
    cur = con.cursor()
    # 查询每个城市的车辆数量
    sql = "select 变速箱, count(变速箱) from che168 where 变速箱 != 'None' group by 变速箱"
    data = cur.execute(sql)
    for item in data:
        gearbox.append(str(item[0]))
        num.append(item[1])
        print(gearbox, num)
    cur.close()
    con.close()
    return render_template('gearbox.html', gearbox=gearbox, num=num)


# 排放标准页面
@app.route('/emission')
def emission():
    emission = []  # 排放标准
    num = []  # 车辆数量
    con = sqlite3.connect("che168.db")
    cur = con.cursor()
    # 查询每个标准的车辆数量
    sql = "SELECT 排放标准, COUNT(排放标准) FROM che168 WHERE 排放标准 != 'None' GROUP BY 排放标准"
    data = cur.execute(sql)
    for item in data:
        emission.append(str(item[0]))
        num.append(item[1])
    cur.close()
    con.close()
    return render_template('emission.html', emission=emission, num=num)


# 价格折线图
@app.route('/get_price_data')
def get_price_data():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('che168.db')
    cursor = conn.cursor()

    # 执行查询并统计不同价格区间车辆的数量
    sql = "SELECT CASE WHEN 售价 BETWEEN 0 AND 1 THEN '0-1' WHEN 售价 BETWEEN 1 AND 10 THEN '1-10' WHEN 售价 BETWEEN 11 AND 20 THEN '11-20' WHEN 售价 BETWEEN 21 AND 30 THEN '21-30' WHEN 售价 BETWEEN 31 AND 50 THEN '31-50' WHEN 售价 BETWEEN 51 AND 70 THEN '51-70' WHEN 售价 BETWEEN 71 AND 98 THEN '71-99' ELSE '100+' END AS 价格区间, COUNT(*) AS 数量 FROM che168 WHERE 售价 IS NOT NULL GROUP BY 价格区间 ORDER BY MIN(售价)"
    data = cursor.execute(sql).fetchall()

    # 关闭连接
    conn.close()

    # 处理数据，准备绘图所需的格式
    price_ranges = [item[0] for item in data]
    quantities = [item[1] for item in data]

    # 将数据转换为 JSON 格式并返回
    return jsonify({'price_ranges': price_ranges, 'quantities': quantities})


# 定义一个路由，用于显示包含 ECharts 的页面
@app.route('/price')
def price():
    return render_template('price.html')


if __name__ == '__main__':
    app.run()
