from flask import Flask
from calc import calc_blueprint
from tax import tax_blueprint

app = Flask(__name__)

app.register_blueprint(calc_blueprint)
app.register_blueprint(tax_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
