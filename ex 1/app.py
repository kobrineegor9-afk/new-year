from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    con = sqlite3.connect('data.db')
    cursor = con.cursor()


    return cursor
get_db()

@app.route('/')
def index():
    conn=get_db()
    table_name = 'medicines'
    conn.execute('select * from medicines')
    columns = [description[0] for description in conn.description]
    rows = conn.fetchall()
    conn.close()

    return render_template('index.html',
                           table_name = table_name,
                           columns = columns,
                           rows = rows)

@app.route('/search/')
def search():
    first = request.args.get('select')
    second = request.args.get('text')
    conn = get_db()
    conn.execute('select * from medicines')
    columns = [description[0] for description in conn.description]
    rows = conn.fetchall()
    q=''

    for i in range(len(columns)):
        if first == 'по названию':
            conn.execute('select * from medicines where name = ?',
                         (second,))
            q = conn.fetchall()

        elif first == 'по производителю':
            conn.execute('select * from medicines where manufacturer = ?',
                         (second,))
            q = conn.fetchall()

        elif first =='по форме':
            conn.execute('select * from medicines where form = ?',
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

