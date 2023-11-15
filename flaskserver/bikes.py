from flask import Blueprint, Flask, request, jsonify

from .models import Account, AccountBikePost, BikePost
from . import db

bikes = Blueprint("bikes", __name__)
## this gets all bikes. 
@bikes.route("/bikes", methods=["GET"])
def get_all_bikes():
    bikes = BikePost.query.all()
    for idx, i in enumerate(bikes):
        bikes[idx] = i.as_dict()
    ## convert to dict and send back to home
    return jsonify(bikes)

##this gets all userbikes
@bikes.route("/userBikes", methods=["POST"])
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
def see_bike():
    bike_ID = request.args.get('id')
    bike = (BikePost.query.filter_by(id=bike_ID).first()).as_dict()
    return jsonify(bike)

@bikes.route("/addBike", methods=["POST"])
def add_bike():
    dateStolen = request.json.get("dateStolen", None)
    title = request.json.get("title", None)
    picture = request.json.get("encodedPicture", None)
    colour = request.json.get("colour", None)
    model = request.json.get("model", None)
    user_id = request.json.get("user_id")
    
    ## if a location is given, add location to location table TODO

    newBike = BikePost(datestolen=dateStolen, title=title, picture=picture, colour=colour, model=model)
    db.session.add(newBike)
    db.session.commit()

    newAccountBikePost = AccountBikePost(accountid=user_id, postid=newBike.id)

    db.session.add(newAccountBikePost)
    db.session.commit()

    resp = jsonify(success=True)
    return resp

    