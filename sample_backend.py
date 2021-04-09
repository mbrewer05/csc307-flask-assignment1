from flask import Flask, request, jsonify
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

users = { 
    'users_list' :
    [
        { 
            'id' : 'xyz789',
            'name' : 'Charlie',
            'job': 'Janitor',
        },
        {
            'id' : 'abc123', 
            'name': 'Mac',
            'job': 'Bouncer',
        },
        {
            'id' : 'ppp222', 
            'name': 'Mac',
            'job': 'Professor',
        }, 
        {
            'id' : 'yat999', 
            'name': 'Dee',
            'job': 'Aspring actress',
        },
        {
            'id' : 'zap555', 
            'name': 'Dennis',
            'job': 'Bartender',
        }
    ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['job'] == search_job and user['name'] == search_username:
                        subdict['users_list'].append(user)
            return subdict
        elif search_username:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username:
                        subdict['users_list'].append(user)
            return subdict
        elif search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['job'] == search_job:
                        subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        users['users_list'].append(userToAdd)
        if 'id' not in userToAdd:
            users['users_list'][len(users['users_list'])-1]['id'] = random_id()
        resp = jsonify(users['users_list'][len(users['users_list'])-1])
        resp.status_code = 201 #201 for a successfuly create
        return resp
    elif request.method == 'DELETE':
        userToDel = request.get_json()
        users['users_list'].remove(userToDel)
        resp = jsonify(success=True)
        return resp
    
@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        if id :
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return ({})
        return users
    elif request.method == 'DELETE':
        resp = jsonify(success=True)
        resp.status_code = 404
        for user in users['users_list']:
            if user['id'] == id:
                users['users_list'].remove(user)
                resp.status_code = 204
        return resp

def random_id():
    id = ''
    for i in range(0,3):
        id += chr(random.randrange(97,123))
    id += str(random.randrange(100,1000))
    return id