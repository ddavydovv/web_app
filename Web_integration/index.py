from config import app, db
from routes.region_route import region_bp
from routes.car_route import car_bp
from routes.area_route import area_bp

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.register_blueprint(region_bp)
    app.register_blueprint(car_bp)
    app.register_blueprint(area_bp)
    app.run()
