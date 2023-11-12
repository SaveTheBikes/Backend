from flask import Blueprint, Flask, request, jsonify

from .models import BikePost
from . import db

bikes = Blueprint("bikes", __name__)

@bikes.route("/bikes", methods=["GET"])
def get_all_bikes():
    bikes = BikePost.query.all()
    for idx, i in enumerate(bikes):
        bikes[idx] = i.as_dict()
    ## convert to dict and send back to home
    return jsonify(bikes)

@bikes.route("/seeBike", methods=["GET"])
def see_bike():
    bike_ID = request.args.get('id')
    bike = (BikePost.query.filter_by(id=bike_ID).first()).as_dict()
    return jsonify(bike)

@bikes.route("/addBike", methods=["POST"])
def add_bike():
    dateStolen = request.json.get("dateStolen", None)
    title = request.json.get("title", None)
    picture = request.json.get("encodedPicture", None)

    ## todo we also need to add in the functionality where users ids and bike ids are added to accountbikeposts

    newBike = BikePost(datestolen=dateStolen, title=title, picture=picture)
    db.session.add(newBike)
    db.session.commit()
    resp = jsonify(success=True)
    return resp

    