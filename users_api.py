import flask
from flask import request, jsonify
from data.db_session import create_session
from data.users import User

bp = flask.Blueprint("users_api", __name__, template_folder="templates")


@bp.route("/api/users")
def get_users():
    session = create_session()
    users = session.query(User).all()
    return jsonify({
        "users": [user.to_dict(only=[
            "id", "surname", "name", "age",
            "position", "speciality", "address",
            "email", "hashed_password", "modified_date"
        ]) for user in users]
    })


@bp.route("/api/users/<int:user_id>")
def get_user(user_id: int):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({
            "error": "Job not found"
        })
    else:
        return jsonify({
            "users": user.to_dict(only=[
                "id", "surname", "name", "age",
                "position", "speciality", "address",
                "email", "hashed_password", "modified_date"
            ])
        })


@bp.route("/api/users/add", methods=['POST'])
def add_user():
    valid = [
        "id", "surname", "name", "age",
        "position", "speciality", "address",
        "email", "password"
    ]
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in valid):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    if session.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'])
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@bp.route("/api/users/edit/<int:user_id>", methods=['POST'])
def user_edit(user_id: int):
    valid = ["surname", "name", "age",
             "position", "speciality", "address",
             "email", "password"]
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = create_session()
    user = session.query(User).filter(User.id == user_id)
    if not user.first():
        return jsonify({'error': 'Not found'})
    edits = {}
    for j in request.json:
        if j in valid:
            edits[j] = request.json[j]
    user.update(edits)
    session.commit()
    return jsonify({'success': 'OK'})


@bp.route("/api/users/delete/<int:user_id>", methods=['DELETE'])
def delete_user(user_id: int):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})
