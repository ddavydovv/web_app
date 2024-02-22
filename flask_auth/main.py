import os
from __init__ import app
from __init__ import db
from app.routes import users


app.register_blueprint(users)


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            print('ok')
    except Exception as e:
        print(f"Error during table creation: {str(e)}")
    app.run(debug=True)
