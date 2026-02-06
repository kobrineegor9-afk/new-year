from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)

con = sqlite3.connect('logins.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT
                last_name TEXT,
                name TEXT,
                patronymic TEXT,
                gender TEXT,
                email TEXT,
                username TEXT,
                password TEXT
             ''')




@app.route('/login/', methods = ['POST', 'GET'])
def index():
    if request.method =='POST':
        login = request.form['login']
        password = request.form['password']
        return f'вы ввели логин{login} и пароль{password}'
    # else:
    #     return'вы уже авторизовались'
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True,port = 5000)