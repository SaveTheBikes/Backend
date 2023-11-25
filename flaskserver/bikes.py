from flask import Blueprint, Flask, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from .models import Account, AccountBikePost, BikePost, BikePostLocation
from . import db

bikes = Blueprint("bikes", __name__)
## this gets all bikes. 
@bikes.route("/allBikes", methods=["GET"])
def get_all_bikes():
    bikes = BikePost.query.all()
    for idx, i in enumerate(bikes):
        bikes[idx] = i.as_dict()
    ## convert to dict and send back to home
    return jsonify(bikes)

##this gets all userbikes
@bikes.route("/userBikes", methods=["POST"])
@jwt_required()
def get_user_bikes():
    ## will need to work with accountnameBikes to find which ones belong to user
    ## then use bike table to return those TODO

    userID = request.json.get("userID", None)
    if not userID:
        return jsonify({'message': 'UserID is missing!'}), 403
    user = Account.query.filter_by(id=userID).first()
    if not user:
        return jsonify({'message': 'No user with this ID'}), 403
    
    user_bike_query = db.session.query(BikePost).\
        join(AccountBikePost, AccountBikePost.postid == BikePost.id).\
        filter(AccountBikePost.accountid == userID)
    
    user_bikes = user_bike_query.all()

    for idx, i in enumerate(user_bikes):
        user_bikes[idx] = i.as_dict()

    return jsonify(user_bikes)

@bikes.route("/seeBike", methods=["GET"])
@jwt_required()
def see_bike():
    bike_ID = request.args.get('id')
    bike = (BikePost.query.filter_by(id=bike_ID).first()).as_dict()
    return jsonify(bike)

@bikes.route("/bikeSpotting", methods=["POST"])
@jwt_required()
def spot_bike():
    bike_ID = request.args.get('id')
    locationlat = request.args.get('locationlat')
    locationlon = request.args.get('locationlon')
    dateseen = request.args.get('dateseen')
    address = request.args.get('address')

    try:
        newLocation = BikePostLocation(locationlon=locationlon, locationlat=locationlat, postid=bike_ID, address=address, dateseen=dateseen)
        db.session.add(newLocation)
        db.session.commit(newLocation)
        resp = jsonify(success=True)

    except SQLAlchemyError as e:
        # Roll back our changes if epic fail
        db.session.rollback()
        resp = jsonify(success=False, error=str(e))
    
    return resp
    
@bikes.route("/addBike", methods=["POST"])
@jwt_required()
def add_bike():
    dateStolen = request.json.get("dateStolen", None)
    title = request.json.get("title", None)
    picture = request.json.get("encodedPicture", None)
    colour = request.json.get("colour", None)
    model = request.json.get("model", None)
    user_id = request.json.get("userID")

    locationlat = request.json.get("location_lat", None)
    locationlon = request.json.get("location_lon", None)
    dateseen = request.json.get("dateseen", None)
    address = request.json.get("address", None)

    try:
        # Create a new BikePost instance and add it to the session
        newBike = BikePost(datestolen=dateStolen, title=title, picture=picture, colour=colour, model=model)
        db.session.add(newBike)
        
        # The 'flush' method sends the above SQL command to the database, 
        # and the 'id' for newBike is populated, but it doesn't commit yet
        db.session.flush()

        # Now that the newBike has an ID, create a new AccountBikePost instance
        newAccountBikePost = AccountBikePost(accountid=user_id, postid=newBike.id)
        db.session.add(newAccountBikePost)

        # Add to location table if we have coordinates
        if locationlat and locationlon:
            newLocation = BikePostLocation(locationlon=locationlon, locationlat=locationlat, postid=newBike.id, address=address, dateseen=dateseen)
            db.session.add(newLocation)

        # Commit the transaction
        db.session.commit()
        resp = jsonify(success=True)
    except SQLAlchemyError as e:
        # Roll back our changes if epic fail
        db.session.rollback()
        resp = jsonify(success=False, error=str(e))
        
    return resp

    
