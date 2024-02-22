from flask import Blueprint, request, jsonify

calc_blueprint = Blueprint('calc_blueprint', __name__)

# Создадим словарь для хранения данных
data_calc = {'reg_id': [],
             'tax_rate': []}


@calc_blueprint.route('/v1/fetch/calc', methods=['GET'])
def fetch_calc():
    data_2 = request.get_json()
    reg_id = data_2.get('reg_id')
    price = data_2.get('price')
    mounth = data_2.get('mounth')
    if data_calc['reg_id'] != reg_id:
        return jsonify({'ERROR': 'Такого reg_id нет в словаре'}), 400
    else:
        tax = data_calc['tax_rate'] * price * mounth / 12
        return jsonify({'Налог за год': tax})
