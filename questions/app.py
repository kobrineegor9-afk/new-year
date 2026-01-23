from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/find/')
def page_index():
    return render_template('index.html')


# @app.route('/result_find/')
# def find_page():
#     name = request.args.get('name')
#     age = request.args.get('age')
#     return f'вы искали по имени {name} и по возрасту {age}'


@app.route('/result_find/')
def find_page():
    text = request.args.get('text')
    type_find = request.args.get('type_find')
    return f'вы искали по {type_find} {text}'
app.run(debug=True)