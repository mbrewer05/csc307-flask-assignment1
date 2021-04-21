from flask import Flask, request, jsonify
from flask_cors import CORS
# import random
import json
from model_mongodb import User

app = Flask(__name__)
CORS(app)

users = {
    'users_list': []
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            users = User().find_by_name_job(search_username, search_job)
        elif search_username:
            users = User().find_by_name(search_username)
        elif search_job:
            users = User().find_by_job(search_job)
        else:    
            users = User().find_all()
        return {"users_list": users}
    elif request.method == 'POST':
        userToAdd = request.get_json()
        newUser = User(userToAdd)
        newUser.save()
        resp = jsonify(newUser), 201
        return resp
    # elif request.method == 'DELETE':
    #     userToDel = request.get_json()
    #     users['users_list'].remove(userToDel)
    #     resp = jsonify(success=True)
    #     return resp
    
@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        user = User({"_id": id})
        if user.reload():
            return user
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        user = User({"_id": id})
        if user.reload():
            user.remove()
        return jsonify({"error": "User not found"}), 404

# def random_id():
#     id = ''
#     for i in range(0,3):
#         id += chr(random.randrange(97,123))
#     id += str(random.randrange(100,1000))
#     return id
# 
# def find_users_by_name_job(name, job):
#     subdict = {'users_list': []}
#     for user in users['users_list']:
#         if user['name'] == name and user['job'] == job:
#             subdict['users_list'].append(user)
#     return subdict
# 
# 
# def find_users_by_job(job):
#     subdict = {'users_list': []}
#     for user in users['users_list']:
#         if user['job'] == job:
#             subdict['users_list'].append(user)
#     return subdict