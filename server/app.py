# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def eqs_by_id(id):
    eq = Earthquake.query.filter(Earthquake.id == id).first()

    if eq is None:
        return {"message": f"Earthquake {id} not found."}, 404
    
    return eq.to_dict(), 200
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def eqs_gte_magnitude(magnitude):
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return {
        'count': len(eqs),
        'quakes': [eq.to_dict() for eq in eqs]
    }, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
