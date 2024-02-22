from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import CarTax, Region, db

car_bp = Blueprint('car_bp', __name__)


@car_bp.route('/v1/car/tax-param/add', methods=['POST'])
def add_car_tax_param():
    data = request.get_json()

    tax_param_id = data.get('id')
    region_id = data.get('city_id')
    from_hp_car = data.get('from_hp_car')
    to_hp_car = data.get('to_hp_car')
    from_production_year_car = data.get('from_production_year_car')
    to_production_year_car = data.get('to_production_year_car')
    rate = data.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    existing_tax_param = CarTax.query.filter_by(
        CarTax.id <= tax_param_id,
        CarTax.city_id <= region_id,
        CarTax.from_hp_car <= from_hp_car,
        CarTax.to_hp_car <= to_hp_car,
        CarTax.from_production_year_car <= from_production_year_car,
        CarTax.to_production_year_car <= to_production_year_car,
    ).first()

    if existing_tax_param:
        return jsonify({"error": "Параметр налога уже существует"}), 400

    new_tax_param = CarTax(
        id=tax_param_id,
        city_id=region_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=from_production_year_car,
        to_production_year_car=to_production_year_car,
        rate=rate,
    )

    try:
        db.session.add(new_tax_param)
        db.session.commit()
        return jsonify({"message": "Параметр налога успешно добавлен"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ошибка целостности"}), 400


@car_bp.route('/v1/car/tax-param/update', methods=['POST'])
def update_car_tax_param():
    data = request.get_json()

    tax_param_id = data.get('id')
    region_id = data.get('city_id')
    from_hp_car = data.get('from_hp_car')
    to_hp_car = data.get('to_hp_car')
    from_production_year_car = data.get('from_production_year_car')
    to_production_year_car = data.get('to_production_year_car')
    rate = data.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    existing_tax_param = CarTax.query.filter_by(
        CarTax.id <= tax_param_id,
        CarTax.city_id <= region_id,
        CarTax.from_hp_car <= from_hp_car,
        CarTax.to_hp_car <= to_hp_car,
        CarTax.from_production_year_car <= from_production_year_car,
        CarTax.to_production_year_car <= to_production_year_car,
    ).first()

    if existing_tax_param and existing_tax_param.id != tax_param_id:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax_param = CarTax.query.get(tax_param_id)

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax_param.city_id = region_id
    tax_param.from_hp_car = from_hp_car
    tax_param.to_hp_car = to_hp_car
    tax_param.from_production_year_car = from_production_year_car
    tax_param.to_production_year_car = to_production_year_car
    tax_param.rate = rate

    db.session.commit()
    return jsonify({"message": "Параметр налога успешно обновлен"}), 200


@car_bp.route('/v1/car/tax-param/delete', methods=['POST'])
def delete_car_tax_param():
    data = request.get_json()

    tax_param_id = data.get('id')

    tax_param = CarTax.query.get(tax_param_id)

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    db.session.delete(tax_param)
    db.session.commit()
    return jsonify({"message": "Налоговый параметр успешно удален"}), 200


@car_bp.route('/v1/car/tax-param/get', methods=['GET'])
def get_car_tax_param():
    tax_param_id = request.args.get('id')

    tax_param = CarTax.query.get(tax_param_id)

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    return jsonify({
        "city_id": tax_param.city_id,
        "from_hp_car": tax_param.from_hp_car,
        "to_hp_car": tax_param.to_hp_car,
        "from_production_year_car": tax_param.from_production_year_car,
        "to_production_year_car": tax_param.to_production_year_car,
        "rate": float(tax_param.rate),
    }), 200


@car_bp.route('/v1/car/tax-param/get/all', methods=['GET'])
def get_all_car_tax_params():
    tax_params = CarTax.query.all()

    result = []
    for tax_param in tax_params:
        result.append({
            "city_id": tax_param.city_id,
            "from_hp_car": tax_param.from_hp_car,
            "to_hp_car": tax_param.to_hp_car,
            "from_production_year_car": tax_param.from_production_year_car,
            "to_production_year_car": tax_param.to_production_year_car,
            "rate": float(tax_param.rate),
        })

    return jsonify(result), 200


@car_bp.route('/v1/car/tax/calc', methods=['GET'])
def calculate_tax():
    region_id = request.args.get('city_id')
    production_year = int(request.args.get('production_year'))
    hp_car = int(request.args.get('hp_car'))

    tax_param = CarTax.query.filter(
        CarTax.city_id == region_id,
        CarTax.from_hp_car <= hp_car,
        CarTax.to_hp_car >= hp_car,
        CarTax.from_production_year_car <= production_year,
        CarTax.to_production_year_car >= production_year
    ).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден по заданным критериям"}), 400

    tax = float(tax_param.rate) * hp_car
    return jsonify({"tax": tax}), 200
