from flask import *
import sqlite3

app = Flask(__name__)
def price_all():
    conn = sqlite3.connect("price_module.db")
    cur = conn.execute("SELECT * FROM prices")
    return (cur.fetchall())
@app.route('/')
def index():
    rows = price_all()
    return render_template("index.html",rows=rows)
@app.route('/add_price',methods=["POST"])
def add_price():
    if request.method == "POST":
        base_price = request.form['base_price']
        base_distance = request.form['base_distance']
        dap = request.form['dap']
        tmf = request.form.getlist('tmf')
        tmf_range = request.form.getlist('tmf_range')
        s1=s2 =""
        for i in tmf:
            s1 = s1+i+','
        for i in tmf_range:
            s2 = s2 + i + ','

        conn = sqlite3.connect("price_module.db")
        conn.execute("INSERT INTO prices(base_price,base_distance,dap,tmf,tmf_range,status)VALUES(?,?,?,?,?,?)",(base_price,base_distance,dap,s1,s2,"Disabled"))
        conn.commit()
        rows = price_all()
        return render_template("index.html",rows=rows)
@app.route('/edit_price/<a>')
def edit_price(a):
    conn = sqlite3.connect("price_module.db")
    cur = conn.execute("SELECT * FROM prices WHERE id=?",(a,))
    price = cur.fetchone()
    rows = price_all()
    return render_template("edit_price.html",price=price)
@app.route("/update_price/<a>",methods=["POST"])
def update_price(a):
    if request.method == "POST":
        base_price = request.form['base_price']
        base_distance = request.form['base_distance']
        dap = request.form['dap']
        tmf = request.form.getlist('tmf')
        tmf_range = request.form.getlist('tmf_range')
        s1 = s2 = ""
        for i in tmf:
            s1 = s1 + i + ','
        for i in tmf_range:
            s2 = s2 + i + ','

        conn = sqlite3.connect("price_module.db")
        conn.execute("UPDATE prices SET base_price=?,base_distance=?,dap=?,tmf=?,tmf_range=? WHERE id=?",(base_price,base_distance,dap,s1,s2,a))
        conn.commit()
        rows = price_all()
        return render_template("index.html",rows=rows)

@app.route('/update_status/<a>',methods=["POST"])
def update_status(a):
    if request.method == 'POST':
        status = request.form['status']
        conn = sqlite3.connect("price_module.db")
        conn.execute("UPDATE prices SET status=? WHERE id=?",(status,a))
        conn.commit()
        rows = price_all()
        return render_template("index.html",rows=rows)
@app.route('/delete_price/<a>')
def delete_price(a):
    conn = sqlite3.connect("price_module.db")
    conn.execute("DELETE * FROM prices WHERE id=?",(a,))
    conn.commit()
    rows=price_all()
    return render_template("index.html",rows=rows)

@app.route('/calculate_price')
def calculate_price():
    dist = int(request.args.get('distance'))
    dura = int(request.args.get('duration'))
    conn = sqlite3.connect("price_module.db")
    cur = conn.execute("SELECT * FROM prices WHERE status=?",("Enabled",))
    row = cur.fetchone()
    d= dist-int(row[2])
    if d>0:
        price=int(row[1])+(d*int(row[3]))
    else:
        price = int(row[1])
    tmf = row[4].split(',')
    tmf.pop(-1)
    tmf_range = row[5].split(',')
    tmf_range.pop(-1)
    tbp=0
    for i in range(len(tmf)):
        if dura > float(tmf_range[i]):
            tbp = float(tmf[i])
            continue
        else:
            tbp=float(tmf[i])
            break
    price = price * tbp
    conn.execute("INSERT INTO bills(distance,duration,amount)VALUES(?,?,?)",(dist,dura,price))
    conn.commit()
    dict = {}
    dict['distance']=dist
    dict['duration'] = dura
    dict['price'] = price
    return jsonify(dict)
@app.route('/bills')
def bills():
    conn = sqlite3.connect("price_module.db")
    cur = conn.execute("SELECT * FROM bills")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run()