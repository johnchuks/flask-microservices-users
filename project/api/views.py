from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from project.api.models import User

from project import db

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    response_object = {
        'status':'success',
        'message':'pong'

    }
    return jsonify(response_object), 200


@user_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = dict(status='fail', message='Invalid request data')
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')

    try:
        user = User.query.filter(email=email).first()

        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = dict(status='success', message='{} was added'.format(email))
            return jsonify(response_object), 201

        else:
            response_object = dict(status='fail', message='Sorry, The user already exist')
            return jsonify(response_object), 400

    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = dict(status='fail', message='Invalid payload')
        return jsonify(response_object), 400


@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = User.get_all()
    users_list = []
    if not users:
        response_object = dict(status='fail', message='No users found')
        return jsonify(response_object), 404
    else:
        for user in users:
            users_obj = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            users_list.append(users_obj)
            response_object = dict(status='success', data=users_list)
            return jsonify(response_object), 200


@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    requested_user = User.query.filter(id=int(user_id)).first()
    try:
        if not requested_user:
            response_object = dict(status='fail', message='user not found')
            return jsonify(response_object), 404

        else:
            response_object = {'status': 'success', 'data': {
                'id': requested_user.id,
                'username': requested_user.username,
                'email': requested_user.email
            }}
            return jsonify(response_object), 200

    except ValueError:
        response_object = dict(status='fail', message='user does not exist')
        return jsonify(response_object), 404
