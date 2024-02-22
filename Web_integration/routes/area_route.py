from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import PropertyTax, Region, db

area_bp = Blueprint('area_bp', __name__)


@area_bp.route('/v1/area/tax-param/add', methods=['POST'])
def add_area_tax_param():
    data = request.get_json()

    region_id = data.get('city_id')
    rate = data.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    new_tax_param = PropertyTax(city_id=region_id, rate=rate)

    try:
        db.session.add(new_tax_param)
        db.session.commit()
        return jsonify({"message": "Параметр налога успешно добавлен"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ошибка целостности"}), 400


@area_bp.route('/v1/area/tax-param/update', methods=['POST'])
def update_area_tax_param():
    data = request.get_json()

    region_id = data.get('city_id')
    rate = data.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    tax_param = PropertyTax.query.filter_by(city_id=region_id).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax_param.rate = rate

    db.session.commit()
    return jsonify({"message": "Параметр налога успешно обновлен"}), 200


@area_bp.route('/v1/area/tax-param/delete', methods=['POST'])
def delete_area_tax_param():
    data = request.get_json()

    region_id = data.get('city_id')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    tax_param = PropertyTax.query.filter_by(city_id=region_id).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    db.session.delete(tax_param)
    db.session.commit()
    return jsonify({"message": "Параметр налога успешно удалён"}), 200


@area_bp.route('/v1/area/tax-param/get', methods=['GET'])
def get_area_tax_param():
    region_id = request.args.get('city_id')

    tax_param = PropertyTax.query.filter_by(city_id=region_id).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    return jsonify({"city_id": tax_param.city_id, "rate": float(tax_param.rate)}), 200


@area_bp.route('/v1/area/tax-param/get/all', methods=['GET'])
def get_all_area_tax_params():
    tax_params = PropertyTax.query.all()

    result = []
    for tax_param in tax_params:
        result.append({"city_id": tax_param.city_id, "rate": float(tax_param.rate)})

    return jsonify(result), 200


@area_bp.route('/v1/area/tax/calc', methods=['GET'])
def calculate_area_tax():
    region_id = request.args.get('city_id')
    cadastre_value = float(request.args.get('cadastre_value'))

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден!"}), 400

    tax_param = PropertyTax.query.filter_by(city_id=region_id).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax = cadastre_value * float(tax_param.rate)
    return jsonify({"tax": tax}), 200
