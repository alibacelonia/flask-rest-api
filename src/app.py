from flask import Flask, request,jsonify
from flask_cors import CORS 
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.json_util import dumps
import json
from bson.objectid import ObjectId

app = Flask(__name__) 
conn = pymongo.MongoClient("mongodb+srv://almie0203:!L0veyou143@cluster0.vh54v.mongodb.net/flaskmongorestful?retryWrites=true&w=majority",connect=False)
  
db = conn.flaskmongorestful


@app.route('/users', methods=['POST', 'GET'])
def get_all_users():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        birthdate = body['birthdate']
        email = body['email']
        password = generate_password_hash(body['password'])

        # db.users.insert_one({
        db['users'].insert_one({
            "name": name,
            "birthdate": birthdate,
            "email": email,
            "password": password,
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            "name": name,
            "birthdate": birthdate,
            "email": email,
            #"password": password,
        })
    
    # GET all data from database
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            name = data['name']
            birthdate = data['birthdate']
            email = data['email']
            #password = data['password']

            dataDict = {
                "id":str(id),
                "name": name,
                "birthdate": birthdate,
                "email": email,
                #"password": password,
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def get_by_id(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        name = data['name']
        birthdate = data['birthdate']
        email = data['email']
        dataDict = {
            "id":str(id),
            "name": name,
            "birthdate": birthdate,
            "email": email,
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        first = body['name']['first']
        middle = body['name']['middle']
        last = body['name']['last']
        birthdate = body['birthdate']
        email = body['email']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "name":{
                        "first":first,
                        "middle":middle,
                        "last":last
                    },
                    "birthdate":birthdate,
                    "email":email
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == "__main__":
    app.run(
        debug=True, 
        port=5001, 
        host='0.0.0.0'
    )