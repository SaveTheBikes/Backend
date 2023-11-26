from flask import Blueprint, Flask, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from .models import Account, AccountBikePost, BikePost
from . import db

bikes = Blueprint("bikes", __name__)
## this gets all bikes. 
@bikes.route("/allBikes", methods=["GET"])
def get_all_bikes():
    bike_posts_with_phone_numbers = db.session.query(
        BikePost, Account.phonenumber
    ).join(
        AccountBikePost, AccountBikePost.postid == BikePost.id
    ).join(
        Account, Account.id == AccountBikePost.accountid
    ).all()

    # Construct the result list with bike details and associated phone numbers
    results = []
    for bike_post, phone_number in bike_posts_with_phone_numbers:
        bike_details = bike_post.as_dict()
        bike_details['phone_number'] = phone_number
        results.append(bike_details)

    return jsonify(results)

##this gets all userbikes
@bikes.route("/userBikes", methods=["POST"])
@jwt_required()
def get_user_bikes():
    ## will need to work with accountnameBikes to find which ones belong to user

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
        user_bikes[idx]["phonenumber"] = user.phonenumber

    return jsonify(user_bikes)

@bikes.route("/seeBike", methods=["GET"])
@jwt_required()
def see_bike():
    bike_ID = request.args.get('id')
    # Ensure you have a valid bike_ID before proceeding with the query

    # Perform a join between the tables to find the phone number associated with the bike post
    bike_with_phone_number = db.session.query(
        BikePost, Account.phonenumber
    ).join(
        AccountBikePost, AccountBikePost.postid == BikePost.id
    ).join(
        Account, Account.id == AccountBikePost.accountid
    ).filter(
        BikePost.id == bike_ID
    ).first()

    if bike_with_phone_number:
        bike, phone_number = bike_with_phone_number
        bike_details = bike.as_dict()
        bike_details['phonenumber'] = phone_number
        return jsonify(bike_details)
    else:
        return jsonify({"error": "Bike not found"}), 404
    
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

    try:
        # Create a new BikePost instance and add it to the session
        newBike = BikePost(datestolen=dateStolen, title=title, picture=picture, colour=colour, model=model, locationlat=locationlat, locationlon=locationlon)
        db.session.add(newBike)
        
        # The 'flush' method sends the above SQL command to the database, 
        # and the 'id' for newBike is populated, but it doesn't commit yet
        db.session.flush()

        # Now that the newBike has an ID, create a new AccountBikePost instance
        newAccountBikePost = AccountBikePost(accountid=user_id, postid=newBike.id)
        db.session.add(newAccountBikePost)

        # Commit the transaction
        db.session.commit()
        resp = jsonify(success=True)
    except SQLAlchemyError as e:
        # Roll back our changes if epic fail
        db.session.rollback()
        resp = jsonify(success=False, error=str(e))
        
    return resp

    
