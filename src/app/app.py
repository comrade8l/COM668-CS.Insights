import json
import time
from flask import Flask, redirect, request, jsonify, make_response, render_template
from bson.json_util import dumps
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from functools import wraps
import bcrypt
import jwt
import re
import datetime
import requests
import logging
import os

app = Flask(__name__)
CORS(app)

# Environment variables
API_KEY = os.getenv('3609C476B1EA443A3DFD2E5B40B6EA28')
CSGO_APP_ID = "730"
MONGO_URI = os.getenv('mongodb://localhost:27017')

client = MongoClient("mongodb://localhost:27017")
# Database name
db = client.cs2
# Collection names
collection_skins = db.skins
# Feedback collection
collection_feedback = db.feedback
#Balcklist collection
blacklist = db.blacklist
#Player stats collection
collection_stats = db.stats
#Staff Collection
collection_staff = db.staff
#CS.Float Database
collection_float = db.float

app.config['SECRET_KEY'] = 'mysecret'

@app.route("/", methods=["POST"])
def handle_root_post():
    return jsonify({"message": "Root POST request received"}), 200

#Find all skins
@app.route("/api/v1.0/skins", methods=["GET"])
def show_all_skins():
    page_num, page_size = 1, 18
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    data_to_return = []
    for skin in collection_skins.find().skip(page_start).limit(page_size):
        skin['_id'] = str(skin['_id'])
        for review in skin['reviews']:
            if len(review) != 0:
                review['_id'] = str(review['_id'])
        data_to_return.append(skin)
    return make_response(jsonify(data_to_return), 200)

#random skin
@app.route("/api/v1.0/skins/random/", methods=["GET"])
def show_all_skins_random():
    time.sleep(2)
    page_size = 5  # Default page size
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    # Using MongoDB's aggregation framework to get random documents
    random_skins = list(collection_skins.aggregate([
        {'$sample': {'size': page_size}}
        
    ]))

    # Preparing data to return
    data_to_return = []
    for skin in random_skins:
        skin['_id'] = str(skin['_id'])
        if 'reviews' in skin:
            for review in skin['reviews']:
                if len(review) != 0:
                    review['_id'] = str(review['_id'])
        data_to_return.append(skin)

    return make_response(jsonify(data_to_return), 200)

# Show one skin from ID
@app.route("/api/v1.0/skins/<string:id>", methods=["GET"])
def show_one_skin(id):
    if len(id) != 24:
        return make_response(jsonify({"error" : "ID was wrong size"}), 404)
    skin = collection_skins.find_one({'_id':ObjectId(id)})
    if skin is not None:
        skin['_id'] = str(skin['_id'])
        for review in skin['reviews']:
            if len(review) != 0:
                review['_id'] = str(review['_id'])
        return make_response(jsonify([skin]), 200)
    else:
        return make_response(jsonify({"error" : "Invalid skin ID"}), 404)

#Get prices of skins for viewing page
@app.route("/api/v1.0/skins/price/<string:id>", methods=["GET"])
def show_price(id):
    try:
        # Validates ID format by attempting to create an ObjectId
        obj_id = ObjectId(id)
    except:
        # If ID format is invalid, return an error response
        return make_response(jsonify({"error": "Invalid ID format"}), 400)

    skin = collection_skins.find_one({'_id': obj_id}, {'price': 1})  # Only fetch price field
    if skin and 'price' in skin:
        # Prepare the price data to be JSON serializable
        price_info = {
            "7_days": skin['price'].get('7_days', {}),
            "30_days": skin['price'].get('30_days', {}),
            "all_time": skin['price'].get('all_time', {})
        }
        return make_response(jsonify({"price": price_info}), 200)
    else:
        return make_response(jsonify({"error": "Invalid skin ID or no price info available"}), 404)

#Delete the skin
@app.route("/api/v1.0/skins/delete/<string:id>", methods=["DELETE"])
def delete_skin(id):
    if id_is_invalid_length(id):
        return make_response(jsonify({"error" : "ID was wrong size"}), 404)
    result = collection_skins.delete_one( { "_id" : ObjectId(id) } )
    if result.deleted_count == 1:
        return make_response( jsonify( {"result" : "skin was successfully deleted"} ), 200)
    else:
        return make_response( jsonify(
            { "error" : "Invalid skin ID" } ), 404)

#Add a review
@app.route("/api/v1.0/skins/<string:id>/reviews", methods=["POST"])
def add_new_review(id):
    new_review = {
        "_id" : ObjectId(),
        "username" : request.form["username"],
        "stars" : request.form["stars"]
    }
    collection_skins.update_one({ "_id" : ObjectId(id) }, { "$push": { "reviews" : new_review } })
    new_review_link = "http://localhost:5000/api/v1.0/skins/" + id + "/reviews/" + str(new_review['_id'])
    return make_response(jsonify({ "url" : new_review_link }), 200)

#Fetch reviews
@app.route("/api/v1.0/skins/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    if len(id) != 24:
        return make_response(jsonify({"error" : "Review ID cannot be found!!"}), 404)
    data_to_return = []
    skins = collection_skins.find_one(
        { "_id" : ObjectId(id) },
        { "reviews" : 1, "_id" : 0 }
    )
    for review in skins["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)
    return make_response(jsonify(data_to_return), 200)

#Fetch one review
@app.route("/api/v1.0/skins/<gid>/reviews/<rid>", methods=["GET"])
def fetch_one_review(gid, rid):
    if len(gid) != 24:
        return make_response(jsonify({"error" : "ID was wrong size"}), 404)
    skin = collection_skins.find_one(
        { "reviews._id" : ObjectId(rid) },
        { "_id" : 0, "reviews.$" : 1 }
    )
    if skin is None:
        return make_response(
            jsonify({"error":"Invalid skin ID or review ID"}), 404
        )
    skin['reviews'][0]['_id'] = str(skin['reviews'][0]['_id'])
    return make_response(jsonify(skin['reviews'][0]), 200)

#Update a review
@app.route("/api/v1.0/skins/update/<gid>/reviews/<rid>", methods=["PUT"])
def edit_review(gid, rid):
    edited_review = {
        "reviews.$.username" : request.form["username"],
        "reviews.$.stars" : request.form['stars']
    }
    collection_skins.update_one(
        { "reviews._id" : ObjectId(rid) },
        { "$set" : edited_review }
    )
    edit_review_url = "http://localhost:5000/api/v1.0/skins/" + gid + "/reviews/" + rid
    return make_response(jsonify({"url":edit_review_url}), 200)

#Delete a review
@app.route("/api/v1.0/skins/delete/<gid>/reviews/<rid>", methods=["DELETE"])
def delete_review(gid, rid):
    collection_skins.update_one(
        { "_id" : ObjectId(gid) },
        { "$pull" : { "reviews" : { "_id" : ObjectId(rid) } } }
    )
    return make_response(jsonify({}), 200)

#Search for a skin
@app.route('/api/v1.0/skins/search', methods=['GET'])
def search():
  name = request.args.get('name')
  if not name:
    return make_response(jsonify({"error": "No search term provided"}), 400)

  regex_query = re.compile(re.escape(name), re.IGNORECASE)
  results = collection_skins.find({"name": regex_query})  # Adjusted field name
  data_to_return = format_results(results)

  return make_response(jsonify(data_to_return), 200)

def format_results(results):
  formatted_data = []
  for skin in results:
    skin['_id'] = str(skin['_id'])
    # Removed formatting for 'reviews' field
    formatted_data.append(skin)
  return formatted_data

#Bookmarks
#Show all bookmarks
@app.route("/api/v1.0/skins/bookmarks/<username>", methods=["GET"])
def show_all_skins_in_bookmark(username):
    page_num, page_size = 1, 1000
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = page_size * (page_num - 1)
    data_to_return = []
    for skin in collection_skins.find().skip(page_start).limit(page_size):
        skin['_id'] = str(skin['_id'])
        for bookmarks in skin ['bookmarks']:
            if username not in bookmarks:
                continue
            for review in skin ['reviews']:
                if len(review) != 0:
                    review['_id'] = str(review['_id'])
            data_to_return.append(skin)
    return make_response( jsonify(data_to_return), 200 )

#Add a bookmark
@app.route("/api/v1.0/skins/update/bookmarks/<string:id>", methods=["PUT"])
def add_skin_to_bookmark(id):
    if id_is_invalid_length(id):
        return make_response(jsonify({"error" : "ID was wrong size"}), 404)
    if "bookmark" in request.form:
        skin = collection_skins.find_one({'_id':ObjectId(id)})
        skin['_id'] = str(skin['_id'])
        for bookmarks in skin ['bookmarks']:
            if request.form['bookmark'] in bookmarks:
                return make_response( jsonify(
                    { "error":"User already has skin in library" } ), 404)
        result = collection_skins.update_one( \
            { '_id' : ObjectId(id) }, {
              '$push' : { 'bookmarks' : request.form['bookmark']
            }
        } )
        if result.matched_count == 1:
            edited_business_link = \
            "http://localhost:5000/api/v1.0/skins/bookmarks/" + request.form["bookmark"]
            return make_response( jsonify(
                { "url":edited_business_link } ), 200)
        else:
            return make_response( jsonify(
                { "error":"Invalid skin ID" } ), 404)
    else:
        return make_response( jsonify(
        { "error" : "Missing form data" } ), 404)

def id_is_invalid_length(id):
    return len(id) != 24

# Auth method for routes
def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify( {'message' : 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify( {'message' : 'Token is invalid'}), 401
        bl_token = blacklist.find_one({"token":token})
        if bl_token is not None:
            return make_response(jsonify( {'message' : 'Token has been cancelled'}), 401)
        return func(*args, **kwargs)

    return jwt_required_wrapper

# Admin required
def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if data["admin"]:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify( {'message' : 'Admin access required'}), 401)
    return admin_required_wrapper

# Login
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth:
        user = collection_staff.find_one( {'username':auth.username } )
        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user["password"]):
                token = jwt.encode( {'user' : auth.username, 'admin' : user['admin'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, \
                app.config['SECRET_KEY'])
                return make_response(jsonify( {'token':token.decode('UTF-8')}), 200)
            else:
                return make_response(jsonify( {'message':'Bad password'}), 401)
        else:
            return make_response(jsonify( {'message':'Bad username'}), 401)
    return make_response(jsonify({'message':'Authentication required'}), 401)

# Logout
@app.route('/api/v1.0/logout', methods=["GET"])
@jwt_required
def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token":token})
    return make_response(jsonify( {'message' : 'Logout successful'}), 200)

#Get item sales past 3 days for past 10 years
#change from id= & &time
@app.route('/api/v1.0/skins/test') #change to /api/v1.0/skins/test
def skins():
    url = "http://csgobackpack.net/api/GetItemPrice/?id=AK-47 | Wasteland Rebel (Battle-Scarred)&time=7&extend=false&full=false&currency=GBP&icon=true"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return make_response((response.text), 200)

#get link for skins
@app.route('/api/skin_prices')
def get_skin_prices():
    try:
        response = requests.get('https://csgobackpack.net/api/GetItemsList/v2/', timeout=10)
        data = response.json()

        # Add inspect link for each skin
        for item in data['items']:
            item['inspect_link'] = f"https://steamcommunity.com/market/listings/730/{item['market_hash_name']}"

        return jsonify(data)
    except requests.Timeout:
        return jsonify({'error': 'Request timed out'}), 504

#Add skins to database
@app.route('/populate_skins', methods=['GET'])
def populate_skins():
    # Fetch data from the external API
    response = requests.get('https://csgobackpack.net/api/GetItemsList/v2/')
    if response.status_code == 200:
        data = response.json()

        # Assuming the data structure includes an 'items_list' key
        items_list = data.get('items_list', {}).values()  # Adjust based on actual structure

        # Prepare documents for MongoDB insertion
        documents = []
        for item in items_list:
            document = {
                "name": item.get('name'),  # Ensure these keys match the actual response structure
                "market_hash_name": item.get('markethashname'),  # Example additional field, adjust as needed
                "price": item.get('price'),
                "rarity": item.get('rarity'),
                "gun_type": item.get('gun_type'),
                "exterior": item.get('exterior'),
                "type": item.get('type'),
                "class_id": item.get('classid'),
                "tradable": item.get('tradable'),
                "first_sale_date": item.get('first_sale_date'),
                "icon_url": item.get('icon_url'),
                "bookmarks": [],  # Empty array for bookmarks
                "reviews": []  # Empty array for reviews

            }
            documents.append(document)

        # Insert documents into MongoDB
        if documents:
            collection_skins.insert_many(documents)
            return jsonify({"message": f"Successfully inserted {len(documents)} items."}), 200
        else:
            return jsonify({"message": "No items found in the external API response."}), 404
    else:
        return jsonify({"error": "Failed to fetch data from external API"}), response.status_code

#Get player stats
@app.route('/get_csgo_weapon_segments')
def get_csgo_weapon_segments():
    url = "https://public-api.tracker.gg/v2/csgo/standard/profile/steam/76561198008049283/segments/weapon"
    headers = {
        "TRN-Api-Key": "7b8ae3e8-c1ba-46d4-9d1f-9f174e578e3f",
        "Accept": "application/json",
        "Accept-Encoding": "gzip"
    }

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")  # For debugging
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        # For debugging: log response text to understand the error
        print(f"Error: {response.text}")
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code, "message": response.text}), response.status_code

#Leave review for website
@app.route("/api/v1.0/feedback", methods=["POST"])
def add_new_feedback():
  # Create the review document
  new_review = {
    "username": request.form["username"],
    "description": request.form["description"],  # Include description field
    "stars": request.form["stars"],
  }

  # Insert the review into the collection_feedback
  collection_feedback.insert_one(new_review)

  # Create a link to access the new review
  new_review_link = f"http://localhost:5000/api/v1.0/feedback/{id}/reviews/{str(new_review)}"

  # Return the link to the new review
  return make_response(jsonify({"url": new_review_link}), 200)

#Display all feedback

@app.route("/api/v1.0/feedback", methods=["GET"])
def get_feedback():
    # Fetch all reviews from the collection_feedback
    reviews = collection_feedback.find({})

    # Convert the query result to a list of dictionaries
    reviews_list = list(reviews)

    # Convert the list of dictionaries to a JSON string
    # Use dumps from bson.json_util to properly format ObjectId and dates
    reviews_json = dumps(reviews_list)

    # Return the JSON string as a response
    return make_response(reviews_json, 200)


#Gun Types Division

#Rifles
@app.route("/api/v2.0/skins/rifles", methods=["GET"])
def show_all_rifle():
    page_num, page_size = 1, 12
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    
    # Define the gun types to filter skins for
    gun_types = ["AK-47", "AUG", "AWP", "FAMAS", "GALIL AR", "M4A1-S"]

    # Calculate the number of documents to sample based on the page size and page number
    sample_size = page_size * page_num

    # Perform aggregation to filter by gun types, randomize order, and limit the result size
    aggregation_pipeline = [
        {"$match": {"gun_type": {"$in": gun_types}}},  # Filter documents by gun types
        {"$sample": {"size": sample_size}},  # Randomly sample documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Since $sample does not support direct pagination, we manually implement it by slicing the result
    # This method is not efficient for large page numbers but is necessary due to the nature of $sample
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for skin in paginated_documents:
        skin['_id'] = str(skin['_id'])
        for review in skin.get('reviews', []):
            if len(review) != 0:
                review['_id'] = str(review['_id'])
        data_to_return.append(skin)

    return make_response(jsonify(data_to_return), 200)

#SMG

@app.route("/api/v2.0/skins/smg", methods=["GET"])
def show_all_smg_skins():
    page_num, page_size = 1, 12
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    
    # Update this list with the specific SMG models in CS2
    smg_types = ["MP5", "UMP-45", "P90", "MAC-10", "MP7"]

    # Calculate the number of documents to sample
    sample_size = page_size * page_num

    # Aggregation pipeline to filter, sample, and paginate SMG skins
    aggregation_pipeline = [
        {"$match": {"gun_type": {"$in": smg_types}}},  # Filter by SMG types
        {"$sample": {"size": sample_size}},  # Random sample of documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Manual pagination after sampling
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for skin in paginated_documents:
        skin['_id'] = str(skin['_id'])
        for review in skin.get('reviews', []):
            if len(review) != 0:
                review['_id'] = str(review['_id'])
        data_to_return.append(skin)

    return make_response(jsonify(data_to_return), 200)


#Heavy

@app.route("/api/v2.0/skins/heavy", methods=["GET"])
def show_all_heavy_skins():
    page_num, page_size = 1, 18
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    # Update this list with the specific heavy weapon models in CS2
    heavy_types = ["Nova", "XM1014", "MAG-7", "Sawed-Off", "M249", "Negev"]

    # Calculate the number of documents to sample
    sample_size = page_size * page_num

    # Aggregation pipeline to filter, sample, and paginate heavy weapon skins
    aggregation_pipeline = [
        {"$match": {"gun_type": {"$in": heavy_types}}},  # Filter by heavy weapon types
        {"$sample": {"size": sample_size}},  # Random sample of documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Manual pagination after sampling
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for skin in paginated_documents:
        skin['_id'] = str(skin['_id'])
        for review in skin.get('reviews', []):
            if review:  # Simplified check for non-empty reviews
                review['_id'] = str(review['_id'])
        data_to_return.append(skin)

    return make_response(jsonify(data_to_return), 200)


#Pistols
@app.route("/api/v2.0/skins/pistols", methods=["GET"])
def show_all_pistol_skins():
    page_num, page_size = 1, 18
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    # if request.args.get('sort'):
    #     if request.args.get('sort').upper() == "ASC":
    #         sort_order = 1
    #     else: 
    #         sort_order = -1

    # Update this list with the specific Pistol models in CS2
    pistol_types = ["Glock-18", "USP-S", "P250", "Desert Eagle", "Five-SeveN", "Tec-9", "CZ75-Auto", "R8 Revolver"]

    # Calculate the number of documents to sample
    sample_size = page_size * page_num

    # Aggregation pipeline to filter, sample, and paginate pistol skins
    aggregation_pipeline = [
        {"$match": {"gun_type": {"$in": pistol_types}}},  # Filter by pistol types
        {"$sample": {"size": sample_size}},  # Random sample of documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Manual pagination after sampling
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for skin in paginated_documents:
        skin['_id'] = str(skin['_id'])
        for review in skin.get('reviews', []):
            if review:  # Simplified check for non-empty reviews
                review['_id'] = str(review['_id'])
        data_to_return.append(skin)

    return make_response(jsonify(data_to_return), 200)

#Container

@app.route("/api/v2.0/skins/containers", methods=["GET"])
def show_all_containers():
    page_num, page_size = 1, 12
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    # Adjusting criteria to filter by type "Container"
    type_criteria = {"type": "Container"}

    # Calculate the number of documents to sample based on the request
    sample_size = page_size * page_num

    # Aggregation pipeline to filter, sample, and paginate containers
    aggregation_pipeline = [
        {"$match": type_criteria},  # Filter by type "Container"
        {"$sample": {"size": sample_size}},  # Random sample of documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Implement manual pagination after sampling due to $sample behavior
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for container in paginated_documents:
        container['_id'] = str(container['_id'])
        # Assuming 'reviews' or similar fields might not apply to containers
        data_to_return.append(container)

    return make_response(jsonify(data_to_return), 200)

#Stickers
@app.route("/api/v2.0/skins/stickers", methods=["GET"])
def show_all_stickers():
    page_num, page_size = 1, 12
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))

    # Using a regex query to find items with 'Sticker' in the name
    name_criteria = {"name": {"$regex": "Sticker", "$options": "i"}}  # Case-insensitive search

    # Calculate the number of documents to sample based on the request
    sample_size = page_size * page_num

    # Adjust the aggregation pipeline for the regex criteria
    aggregation_pipeline = [
        {"$match": name_criteria},  # Filter by name containing 'Sticker'
        {"$sample": {"size": sample_size}},  # Random sample of documents
    ]

    data_to_return = []
    sampled_documents = list(collection_skins.aggregate(aggregation_pipeline))

    # Implement manual pagination after sampling due to $sample behavior
    start_index = (page_size * (page_num - 1))
    end_index = start_index + page_size
    paginated_documents = sampled_documents[start_index:end_index]

    for sticker in paginated_documents:
        sticker['_id'] = str(sticker['_id'])
        # Here, process any additional fields specific to stickers
        data_to_return.append(sticker)

    return make_response(jsonify(data_to_return), 200)

#SteamAPI (get player stats using steam API key and App ID)
@app.route("/api/v2.0/playerstats/<id>")
def get_player_stats(id):
    api_key = "3609C476B1EA443A3DFD2E5B40B6EA28"
    csgo_app_id="730"
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={csgo_app_id}&key={api_key}&steamid={id}"

    response = requests.request("GET", url)

    return make_response(response.text, 200)
    

#Put data into MongoDB
@app.route("/api/v2.0/playerstats/import/<id>")
def get_player_stats_mongo(id):
    api_key = "3609C476B1EA443A3DFD2E5B40B6EA28"
    csgo_app_id = "730"
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={csgo_app_id}&key={api_key}&steamid={id}"

    response = requests.request("GET", url)
    if response.status_code == 200:
        # Convert response to JSON
        data = response.json()

        # Reorganize data to a more structured format
        structured_data = {
            'steamID': data['playerstats']['steamID'],
            'gameName': data['playerstats']['gameName'],
            'stats': {stat['name']: stat['value'] for stat in data['playerstats']['stats']},
            'achievements': {achievement['name']: achievement['achieved'] for achievement in data['playerstats'].get('achievements', [])}
        }

        # Insert data into MongoDB
        collection_stats.insert_one(structured_data)

        return make_response(json.dumps(structured_data), 200)
    else:
        return make_response(f"Failed to fetch data from Steam API: {response.status_code}", response.status_code)


#Find all Stats
@app.route("/api/v2.0/stats", methods=["GET"])
def show_all_stats():
    page_num, page_size = 1, 18
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    data_to_return = []
    for skin in collection_stats.find().skip(page_start).limit(page_size):
        skin['_id'] = str(skin['_id'])
        data_to_return.append(skin)
    return make_response(jsonify(data_to_return), 200)

#CS.Float API
#Get data from CSFloat API
@app.route("/populate_float", methods=["GET"])
def fetch_csfloat_listings():
    url = "https://csfloat.com/api/v1/listings"
    payload = {}
    headers = {}

    try:
        # Fetch data from CSFloat API
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()

            # Assuming the data is a list of listings, directly insert into MongoDB
            if isinstance(data, list):
                # Insert each listing as a separate document
                insert_result = collection_float.insert_many(data)
                if insert_result.acknowledged:
                    return jsonify({"success": True, "message": f"Data saved to MongoDB, inserted count: {len(insert_result.inserted_ids)}"}), 200
                else:
                    return jsonify({"success": False, "message": "Failed to save data to MongoDB"}), 500
            else:
                # Handle unexpected data format
                return jsonify({"success": False, "message": "Unexpected data format from CSFloat API"}), 500
        else:
            return jsonify({"success": False, "message": "Failed to fetch data from CSFloat API", "status_code": response.status_code}), response.status_code
    except requests.RequestException as e:
        return jsonify({"success": False, "message": "Request to CSFloat API failed", "error": str(e)}), 500

#Get data from mongoDB
@app.route("/api/v1.0/skins/float", methods=["GET"])
def show_all_float():
    page_num, page_size = 1, 50
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    data_to_return = []
    for skin in collection_float.find().skip(page_start).limit(page_size):
        skin['_id'] = str(skin['_id'])
        data_to_return.append(skin)
    return make_response(jsonify(data_to_return), 200)

#Debugging
if __name__ == "__main__":
    app.run(debug=True)
