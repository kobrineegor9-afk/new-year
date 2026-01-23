from flask import Flask, render_template
from project.oracle import get_oracle
app = Flask(__name__)

prediction_counter = 0

@app.route('/')
def page_index():
    global prediction_counter

    oracle = get_oracle()

    prediction_counter += 1
    return render_template(
        'index.html',
        oracle = oracle,
        prediction_counter = prediction_counter
    )
def get_oracle_color(oracle):
    secret_num = 0
    for k,v in oracle.items():
        secret_num += len(k) + len(v)
    random_num = random.randint(100000, 111111)
    return str(secret_num % 10 * random_num)


app.run(debug=True)