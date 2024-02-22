from flask import Blueprint, request

from database import Region
from database import db

region_bp = Blueprint('region', __name__, url_prefix='/v1/region')


@region_bp.route('/add', methods=['POST'])
def add_region():
    region_id = request.json.get('id')
    name = request.json.get('name')

    existing_region = Region.query.filter_by(id=region_id).first()
    if existing_region:
        return {'message': 'Регион уже существует!'}, 400

    region = Region(id=region_id, name=name)
    db.session.add(region)
    db.session.commit()

    return {'message': 'Регион успешно добавлен'}, 200


@region_bp.route('/update', methods=['POST'])
def update_region():
    region_id = request.json.get('id')
    name = request.json.get('name')

    region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {'message': 'Регион не найден!'}, 400

    region.name = name
    db.session.commit()

    return {'message': 'Регион успешно обновлён'}, 200


@region_bp.route('/delete', methods=['POST'])
def delete_region():
    region_id = request.json.get('id')

    region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {'message': 'Регион не найден!'}, 400

    db.session.delete(region)
    db.session.commit()

    return {'message': 'Регион успешно удалён'}, 200


@region_bp.route('/get', methods=['GET'])
def get_region():
    region_id = request.args.get('id')
    region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {'message': 'Регион не найден!'}, 400

    return {'id': region.id, 'name': region.name}, 200


@region_bp.route('/get/all', methods=['GET'])
def get_all_regions():
    regions = Region.query.all()
    regions_data = [{'id': region.id, 'name': region.name} for region in regions]
    return {'regions': regions_data}, 200
