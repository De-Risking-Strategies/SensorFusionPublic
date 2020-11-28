##Flask Routes
import json
import sqlite3
from flask import Flask, request, jsonify

# curl --data "firstName='Drew'&lastName='Anderson'&email='danderson@cloudmediaworks.com'&captureLimit=5" http://localhost:5000/api/user
# curl --data "firstName='Galan'&lastName='Bridgman'&email='gbridgman@cloudmediaworks.com'&captureLimit=5" http://localhost:5000/api/user
# curl --data "firstName='Don'&lastName='Kadish'&email='dkadish@cloudmediaworks.com'&captureLimit=5" http://localhost:5000/api/user


app = Flask(__name__)


@app.route('/api/user', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        all_users = get_all_users()
        return json.dumps(all_users)
    elif request.method == 'POST':
        data = request.form
        result = add_user(data['firstName'], data['lastName'], data['email'], data['captureLimit'])
        return jsonify(result)



@app.route('/api/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(user_id):
    if request.method == 'GET':
        user = get_single_user(user_id)
        return json.dumps(user)
    elif request.method == 'PUT':
        data = request.form
        result = edit_user(
            user_id, data['firstName'], data['lastName'],  data['email'], data['captureLimit'])
        return jsonify(result)
    elif request.method == 'DELETE':
        result = delete_user(user_id)
        return jsonify(result)


# helper functions

def add_user(firstName, lastName, email, captureLimit):
    try:
        with sqlite3.connect('sf.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO user (firstName, lastName, email, captureLimit) values (?, ?, ?, ?);
                """, (firstName, lastName, email, captureLimit,))
            result = {'status': 1, 'message': 'User Added'}
    except:
        result = {'status': 0, 'message': 'error'}
    return result


def get_all_users():
    with sqlite3.connect('sf.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user ORDER BY id desc")
        all_users = cursor.fetchall()
        return all_users


def get_single_user(user_id):
    with sqlite3.connect('sf.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user


def edit_user(user_id, firstName, lastName, email, captureLimit):
    try:
        with sqlite3.connect('sf.db') as connection:
            connection.execute("UPDATE user SET firstName = ?, lastName = ?,  email = ?, captureLimit = ? WHERE ID = ?;", (firstName, lastName, email, captureLimit, user_id,))
            result = {'status': 1, 'message': 'USER Edited'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


def delete_user(user_id):
    try:
        with sqlite3.connect('sf.db') as connection:
            connection.execute("DELETE FROM user WHERE ID = ?;", (user_id,))
            result = {'status': 1, 'message': 'USER Deleted'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
