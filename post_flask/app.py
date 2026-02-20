from flask import Flask,render_template,request,flash
import sqlite3
app = Flask(__name__)
app.secret_key = '1234'


def get_db():
    conn = sqlite3.connect('logins.db')
    cursor = conn.cursor()
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
    conn.commit()
    return conn



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login/', methods = ['POST', 'GET'])
def register():


    return render_template('register.html')

@app.route('/register/', methods = ['POST','GET'])
def save_register():
    conn = get_db()
    cursor = conn.cursor()

    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        last_name = request.form['last_name']
        name = request.form['name']
        gen = request.form['gen']
        patronymic = request.form['patronymic']
        email = request.form['email']
        n_p =(last_name, name, patronymic, gen, email,username,password)
        cursor.execute('''insert into users(last_name, name, patronymic, gen , email,username,password) values (?,?,?,?,?,?,?);''',n_p)
        conn.execute('select * from users')
        conn.commit()
        cursor.execute('select * from users')
        q = cursor.fetchall()
        print(q)

        return f'{username} вы успешно зарегестрировались'

@app.route('/autorisation/', methods = ['POST', 'GET'])
def autorisation():
    return render_template('auto.html')

@app.route('/check_auto/', methods = ['POST','GET'])
def check_auto():
    conn = get_db()
    cursor = conn.cursor()
    if request.method =='POST':
        uname = request.form['username']
        password = request.form['password']
        print(uname)
        print(password)
        cursor.execute('SELECT * FROM users WHERE username=? AND password = ?',
                       (uname, password))
        user = cursor.fetchall()
        if user:
            return f'добро пожаловать {user[2]}{user[1]}!'
        else:
            cursor.execute('SELECT * FROM users WHERE username=?',
                           (uname,))
            existing_user = cursor.fetchone()

            if existing_user:
                return ' неверный пароль'
            else:
                return'пользователь не найден'
    conn.close()

@app.route('/login1/', methods = ['POST', 'GET'])
def reg():
    return render_template('login.html')

@app.route('/auto/', methods = ['POST','GET'])
def autorisation2():
    if request.method == 'POST':
        login = request.form['username']
        if login == '111':
            flash('вы авторизовались', 'success')
        else:
            flash("неверный лоигн или пароль", 'danger')
            return render_template('login.html')
        return render_template('autorization.html')







if __name__=='__main__':
    app.run(debug=True,port = 5000)