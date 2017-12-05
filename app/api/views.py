from flask import Blueprint, jsonify


user_routes = Blueprint('users', __name__)


@user_routes.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status' : 'success',
        'message' : 'pong!'
    })
