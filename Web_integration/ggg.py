from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/my_list')
def my_list():
    items = ['item 1', 'item 2', 'item 3']
    return jsonify(items)


if __name__ == '__main__':
    app.run(debug=True)