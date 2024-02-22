from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(dbname='web-app', user='postgres',
                        password='postgres', host='localhost')
c = conn.cursor()
conn.commit()


@app.route('/v1/add/region', methods=['POST'])
def add_region():
    data = request.get_json()
    name = data.get('name')
    id = data.get('id')
    c.execute("SELECT * FROM region WHERE id = %s", (id,))

    existing_region = c.fetchone()
    if existing_region:
        return jsonify({'error': 'Region with this id already exists'}), 400
    c.execute("INSERT INTO region (id, name) VALUES (%s, %s)", (id, name))
    conn.commit()
    return jsonify({'message': 'Region added successfully'}), 201


@app.route('/v1/add/tax-param', methods=['POST'])
def add_tax_param():
    c = conn.cursor()
    data_1 = request.get_json()
    city_id = data_1.get('city_id')
    from_hp_car = data_1.get('from_hp_car')
    to_hp_car = data_1.get('to_hp_car')
    from_production_year_car = data_1.get('from_production_year_car')
    to_production_year_car = data_1.get('to_production_year_car')
    rate = data_1.get('rate')
    c.execute("SELECT * FROM region WHERE id = %s", (city_id,))
    existing_region = c.fetchone()
    if existing_region is None:
        return jsonify({'ERROR': '400 BAD REQUEST'}), 400
    c.execute("SELECT * FROM tax_param WHERE city_id = %s", (city_id,))
    existing_tax_param = c.fetchone()
    if existing_tax_param:
        return jsonify({'ERROR': '400 BAD REQUEST'}), 400
    else:
        c.execute("INSERT INTO tax_param (city_id, from_hp_car,to_hp_car,from_production_year_car,to_production_year_car,rate)"
                  "VALUES (%s, %s, %s, %s, %s, %s)",
              (city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate))
        conn.commit()
        return 200


@app.route('/v1/add/auto', methods=['POST'])
def add_auto():
    data_2 = request.get_json()
    city_id = data_2.get('city_id')
    name = data_2.get('name')
    horse_power = data_2.get('horse_power')
    production_year = data_2.get('production_year')

    c.execute("SELECT * FROM region WHERE id = %s", (city_id,))
    existing_region = c.fetchone()

    if existing_region is None:
        return jsonify({'ERROR': '400 BAD REQUEST'}), 400

    c.execute("""SELECT rate, id FROM tax_param WHERE %(horse_power)s >= from_hp_car
              AND %(horse_power)s <= to_hp_car
              AND %(production_year)s >= from_production_year_car 
              AND %(production_year)s <= to_production_year_car""",
              {'horse_power': horse_power, 'production_year': production_year})

    rate = c.fetchone()
    print(rate)
    if rate is None:
        return jsonify({'ERROR': '400 BAD REQUEST'}), 400

    tax = rate[0] * horse_power

    c.execute(
        "INSERT INTO auto (tax_id, city_id, name, horse_power, production_year, tax)"
        " VALUES (%s, %s, %s, %s, %s, %s)",
        (rate[1], city_id, name, horse_power, production_year, tax))

    conn.commit()

    return jsonify({'message': 'Data added successfully'})


@app.route('/v1/auto', methods=['GET'])
def get_auto():
    data_3 = request.get_json()
    id = data_3.get('id')
    c.execute('SELECT * FROM auto WHERE id = %s', (id,))
    auto_inf = c.fetchone()
    if not auto_inf:
        return jsonify({'error': 'Автомобиль с указанным идентификатором не найден'}), 400

    response_3 = {
        "id": auto_inf[0],
        "city_id": auto_inf[1],
        "name": auto_inf[3],
        "tax_id": auto_inf[2],
        "horse_power": auto_inf[4],
        "production_year": auto_inf[5],
        "tax": auto_inf[6]
    }
    c.close()
    return jsonify(response_3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

conn.commit()

