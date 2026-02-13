from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)



def get_db():
    con = sqlite3.connect('logins.db')
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT,
                    name TEXT,
                    patronymic TEXT,
                    gen TEXT,
                    email TEXT,
                    username TEXT,
                    password TEXT)
                ''')
    return cursor



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login/', methods = ['POST', 'GET'])
def register():


    return render_template('register.html')

@app.route('/register/', methods = ['POST','GET'])
def save_register():
    conn = get_db()
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        last_name = request.form['last_name']
        name = request.form['name']
        gen = request.form['gen']
        patronymic = request.form['patronymic']
        email = request.form['email']
        n_p =(last_name, name, patronymic, gen, email,username,password)
        conn.execute('''insert into users(last_name, name, patronymic, gen , email,username,password) values (?,?,?,?,?,?,?);''',n_p)
        conn.execute('select * from users')
        q = conn.fetchall()
        print(q)

        return f'{username} вы успешно зарегестрировались'

@app.route('/autorisation/', methods = ['POST', 'GET'])
def autorisation():
    return render_template('auto.html')

@app.route('/check_auto/', methods = ['POST','GET'])
def check_auto():
    conn = get_db()
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        if conn.execute('select * from users where username =?',
                        (username,)):
            if conn.execute('select * from users where password =?',
                            (password,username)):
            return 'вы вошли в свой аккаунт'
        else:
            return 'неверный пароль'
    else:
        return 'неверный логин'


        return f'{username} вы успешно зарегестрировались'







if __name__=='__main__':
    app.run(debug=True,port = 5000)