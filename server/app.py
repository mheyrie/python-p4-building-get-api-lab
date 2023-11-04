#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakery = []
    bakeries = Bakery.query.all()
    for bakery in bakeries:
        all_bakery.append(bakery.to_dict())
        response = make_response(
        jsonify(all_bakery),
        200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    response = make_response(jsonify(bakery.to_dict()))
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakeries_by_price = []
    baked_good_price = BakedGood.query.order_by((BakedGood.price).desc()).all()
    for price in baked_good_price:
        bakeries_by_price.append(price.to_dict())
    
    return make_response(jsonify(bakeries_by_price))
            

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by((BakedGood.price).desc()).first()
        
    response = make_response(jsonify(baked_good.to_dict()))
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
