from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)



def get_db():
    conn = sqlite3.connect('tovar.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER,
                    col INTEGER,
                    nal BOOLEAN,
                    tel TEXT)
                ''')
    conn.commit()
    return conn


@app.route('/register/', methods = ['POST','GET'])
def save_register():
    conn = get_db()
    cursor = conn.cursor()
    if request.method =='POST':
        name = request.form['name']
        price = request.form['price']
        col = request.form['col']
        nal = request.form['nal']
        if nal =='True':
            nal = True
        else:
            nal = False
        tel = request.form['tel']
        n_p =(name, price, col, nal, tel)
        cursor.execute('''insert into products(name, price, col, nal, tel) values (?,?,?,?,?);''',n_p)
        conn.commit()
        return f'товар с названием {name} зарегистрирован'




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reg/', methods = ['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/search/')
def search():
    first = request.args.get('select')
    second = request.args.get('text')
    conn = get_db()
    conn.execute('select * from products')
    columns = [description[0] for description in conn.description]
    rows = conn.fetchall()
    q=''

    for i in range(len(columns)):
        if first == 'по названию':
            conn.execute('select * from products where name = ?',
                         (second,))
            q = conn.fetchall()

        elif first == 'по количеству':
            conn.execute('select * from products where col = ?',
                         (second,))
            q = conn.fetchall()

        elif first =='по цене':
            conn.execute('select * from products where price = ?',
                         (second,))
            q = conn.fetchall()
        else:
            q='error'
    conn.close()

    return render_template('search.html',
                           columns=columns,
                           rows=rows,
                           first = first,
                           second = second,
                           q=q)



if __name__=='__main__':
    app.run(debug=True,port = 5000)

