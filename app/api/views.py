from flask import Blueprint, jsonify, request, render_template
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.models import User


user_routes = Blueprint('users', __name__, template_folder='./templates')


@user_routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username, email))
        db.session.commit()
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('index.html', users=users)


@user_routes.route('/users', methods=['POST'])
def new_user():
    payload = request.get_json()
    if not payload:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), 400
    username = payload.get('username')
    email = payload.get('email')
    try:
        db.session.add(User(username, email))
        db.session.commit()
        response_data = dict(status='success', message=f'{email} was added!')
        return jsonify(response_data), 201
    except IntegrityError as e:
        db.session.rollback()
        response = {'status': 'fail'}
        if 'not-null' in str(e):
            response['message'] = 'Invalid payload.'
        else:
            response['message'] = 'Sorry. That email already exists.'
        return jsonify(response), 400


@user_routes.route('/users/<user_id>', methods=['GET'])
def show_user(user_id):
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if user:
            response = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return jsonify(response), 200
    except ValueError:
        pass
    return  jsonify({'status': 'fail', 'message': 'User does not exist'}), 404


@user_routes.route('/users', methods=['GET'])
def index_users():
    users = User.query.all()
    group_of_users = []
    for user in users:
        group_of_users.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        })
    response = {
        'status': 'success',
        'data': {
            'users': group_of_users
        }
    }
    return jsonify(response), 200


@user_routes.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status' : 'success',
        'message' : 'pong!'
    })
