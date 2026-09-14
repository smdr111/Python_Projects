from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import choice

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name : getattr(self,column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def get_random():
    result = db.session.execute(db.select(Cafe))
    cafe = choice(result.scalars().all())
    return jsonify(cafe=cafe.to_dict())


@app.route('/all')
def get_all():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    cafes = result.scalars().all()
    all_cafes = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafe=all_cafes)


@app.route('/search')
def get_location():
    loc_param = request.args.get('loc')
    results = db.session.execute(db.select(Cafe).where(Cafe.location == loc_param)).scalars().all()
    if results:
        return jsonify(cafe=[cafe.to_dict() for cafe in results])
    else:
        error = {'Not Found':'Sorry,we don\'t have cafe at that location.'},404
        return jsonify(error=error)


# HTTP POST - Create Record
@app.route('/add',methods=['POST'])
def add():
    data = request.get_json()
    cafe = Cafe(
        name=data["name"],
        map_url=data["map_url"],
        img_url=data["img_url"],
        location=data["location"],
        seats=data["seats"],
        has_toilet=data["has_toilet"],
        has_wifi=data["has_wifi"],
        has_sockets=data["has_sockets"],
        can_take_calls=data["can_take_calls"],
        coffee_price=data.get("coffee_price")
    )
    db.session.add(cafe)
    db.session.commit()
    return jsonify({
        "message": "Cafe added successfully",
        "cafe": {
            "id": cafe.id,
            "name": cafe.name,
            "location": cafe.location
        }
    }), 201


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>',methods=['PATCH'])
def update_new_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe_to_update = db.session.get(Cafe,cafe_id)
    if cafe_to_update is None:
        return jsonify(error={'Not Found' : 'Cafe not found for update'}),404
    cafe_to_update.coffee_price = new_price
    db.session.commit()
    return jsonify({'Success' : 'Cafe updated succesfully'}),200

# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>',methods=['DELETE'])
def delete(cafe_id):
    key = request.args.get('api-key')
    if key == "TopSecretAPIKey":
        cafe_to_delete = db.session.get(Cafe,cafe_id)
        if cafe_to_delete is None:
            return jsonify(error={'Not Found' : 'Cafe not found for update'}), 404
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify({'Success' : 'Cafe deleted succesfully'}), 200
    else:
        return jsonify({'error': 'Sorry that\'s not allowed make sure you have the correct api_key'}), 403

if __name__ == '__main__':
    app.run(debug=True)
