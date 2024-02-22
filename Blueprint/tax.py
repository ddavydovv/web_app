from flask import request, Blueprint, jsonify

tax_blueprint = Blueprint('tax_blueprint', __name__)

# Создадим словарь для хранения данных
data_dict = {'reg_id': [],
             'tax_rate': []}


@tax_blueprint.route('/v1/add/tax', methods=['POST'])
def add_tax():
    data = request.get_json()
    reg_id = data.get('reg_id')
    tax_rate = data.get('tax_rate')
    if data_dict['reg_id'] == reg_id:
        return jsonify({'ERROR': 'Reg_id существует!'}), 400
    else:
        data_dict['reg_id'] = reg_id
        data_dict['tax_rate'] = tax_rate
        print(data_dict)
        return jsonify({'message': 'Данные добавлены успешно!'})


@tax_blueprint.route('/v1/fetch/taxes', methods=['GET'])
def fetch_taxes():
    return jsonify(data_dict)


@tax_blueprint.route('/v1/fetch/tax', methods=['GET'])
def fetch_tax():
    data_1 = request.get_json()
    reg_id = data_1.get('reg_id')
    if data_dict['reg_id'] == reg_id:
        return data_dict
    else:
        return ({'ERROR': 'Такого reg_id нет в словаре'}), 400


@tax_blueprint.route('/v1/update/tax', methods=['POST'])
def update_tax():
    data_3 = request.get_json()
    reg_id = data_3.get('reg_id')
    tax_rate = data_3.get('tax_rate')
    if data_dict['reg_id'] == reg_id:
        data_dict['tax_rate'] = tax_rate
    else:
        return jsonify({'ERROR': 'Такого reg_id нет в словаре'}), 400
    print(data_dict)
    return jsonify({'SUCCESS': 'Данные обновлены!'}), 200
