from restapi import db, app
from restapi.models import User, ClockInOutHistory
from flask import jsonify

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


@app.route('/api/user/<public_id>', methods=['GET'])
def get_user_by_public_id(public_id):
    user = db.session.query(User).filter_by(id=public_id).first()
    if not user:
        return jsonify({'msg':'can not find user, public_id is '+ public_id})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['birth'] = user.birth
    user_data['dpmt'] = user.dpmt
    user_data['status'] = user.status
    user_data['phone'] = user.phone
    user_data['img_url'] = user.img_url

    return jsonify({'User:':user_data})


@app.route('/api/users', methods=['GET', 'POST'])
def get_all_users():
    users = db.session.query(User)
    if not users:
        return jsonify({'msg':'Error on get all users!'})
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['birth'] = user.birth
        user_data['dpmt'] = user.dpmt
        user_data['status'] = user.status
        user_data['phone'] = user.phone
        user_data['img_url'] = user.img_url
        output.append(user_data)
    return jsonify({'Users':output})


@app.route('/api/clockinout/<public_id>/<operator_id>/<in_or_out>', methods=['GET','Post'])
def clock_in_or_out(public_id, operator_id, in_or_out):
    user = db.session.query(User).filter_by(public_id=public_id).first()
    admin = db.session.query(User).filter_by(public_id=operator_id).first()
    result = ''
    clock_ticket = ClockInOutHistory()

    if user and admin:
        clock_ticket.clock_in_or_out = in_or_out
        clock_ticket.user_id = user.id
        clock_ticket.operator_id = admin.id
    else:
        return jsonify({"code":401,"msg":"User or Operator is Null, please check first."})
    
    if user and admin:
        db.session.add(clock_ticket)
        db.session.commit()
    
    return jsonify({"code":200,"msg":in_or_out +' is sucecess!' + result})


@app.route('/api/get_history/<public_id>/<start_date>/<end_date>', methods=['GET','Post'])
def get_user_history(public_id, start_date, end_date):
    response = {}
    historylist = db.session.query(ClockInOutHistory).\
        outerjoin(User, ClockInOutHistory.user_id==User.id).\
        filter_by(public_id=public_id).all()
    res_item = []
    for item in historylist:
        res_item.append([item.clock_datetime,item.clock_in_or_out])


    return jsonify({"history":res_item})


@app.route('/api/login/<username>/<password>', methods=['GET', 'POST'])
def login(username, password):
    token = "fb351d8d-0c6b-4651-9b35-8aee9b59beff"
    pwd = password
    # pwd = hash(password)
    user = db.session.query(User).\
        filter_by(name=username, hashed_pwd=pwd).\
        first()
    if user:
        return jsonify({"code": 200, "token": token})
    else:
        return jsonify({"code": 401,"msg": "Username or password not invaliable."})
