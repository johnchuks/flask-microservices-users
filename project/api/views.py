from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import exc

from project.api.models import User

from project import db

user_blueprint = Blueprint('users', __name__, template_folder='./templates')


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
        user = User.query.filter_by(email=email).first()
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
            users_obj = dict(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
            users_list.append(users_obj)
            response_object = dict(status='success', data=users_list)
            return jsonify(response_object), 200


@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    requested_user = User.query.filter_by(id=user_id).first()
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


@user_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.order_by(User.created_at.desc()).all()

    return render_template('index.html', users=users)