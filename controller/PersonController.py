# router
from flask import Flask, request, Blueprint, render_template, abort, url_for, redirect, jsonify
from flask import make_response
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
from service import ruz, weather, PersonService
from model import Person
from validator.validator import Validator
from validator.ActiveUser import CurrentUser
from validator.SuperUser import CurrentSuperUser
from config.config import IMAGEPATH
from playhouse.shortcuts import model_to_dict
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/get/schedule/name/<full_name>', methods=['GET'])
def get_schedule(full_name):
    r = ruz.Ruz.get_schedule_by_full_name(full_name.replace('_', ' '))
    if r is not None:
        return jsonify(r), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        abort(400)


@app.route('/get/schedule', methods=['GET'])
def get_schedule_by_id():
    if CurrentSuperUser == CurrentUser:
        return CurrentSuperUser.get_ruz(), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return "Not superuser", 400


@app.route('/get/weather', methods=['GET'])
def get_weather():
    if CurrentSuperUser == CurrentUser:
        return CurrentSuperUser.get_weather(), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return "Not superuser", 400


@app.route('/add/person', methods=['POST'])
def add_person():
    file = request.get_json()
    person = json.loads(file)
    return PersonService.PersonService.create_face(person)


# Not working!
# @app.route('/get/person/face/<face>', methods=['GET'])
# def get_person_by_face(face):
# 	return PersonService.PersonService.find_face(
# 		PersonService.PersonService.save_byte_image(
# 			PersonService.PersonService.convert_str_to_img(face)
# 		)
# 	)


# @app.route('/get/person/json/face', methods=['GET'])
# def get_person_by_face_json():
# 	file = request.get_json()
# 	face = json.loads(file)
# 	out = FaceService.FaceService.find_face(
# 	)


@app.route('/add/active_user', methods=['GET', 'POST'])
def add_active_user():
    if request.method == 'POST':
        image = request.files['file']
        if Validator.is_image(image.stream):
            CurrentUser.update(image)
            if CurrentUser.id is not None:
                return 'ok!', 200
        abort(400)
    return render_template('face.html')


@app.route('/get/active_user', methods=['GET'])
def get_active_user():
    if CurrentUser.id is not None:
        print('test')
        return str(CurrentUser), 200
    else:
        abort(400)


@app.route('/get/person/face', methods=['GET', 'POST'])
def get_person_by_face_no_base():
    if request.method == 'POST':
        image = request.files['file']  # .read()
        print(image.filename)
        if Validator.is_image(image.stream):  # Validator.is_valid_filename(image.filename)
            image.save(IMAGEPATH + secure_filename(image.filename))
            out = PersonService.PersonService.find_face(
                # FaceService.FaceService.save_byte_image(image)
                IMAGEPATH + secure_filename(image.filename)
            )
            if out is not None:
                d = model_to_dict(out)
                del d['face_data']
                print(d)
                # return jsonify(d)
                return d, 200, {'Content-Type': 'application/json; charset=utf-8'}
        abort(400)
    return render_template('face.html')


@app.route('/get/person/id/<identity>', methods=['GET'])
def get_person_by_id(identity):
    out = PersonService.PersonService.get_person_by_id(identity)
    if out is not None:
        d = model_to_dict(out)
        del d['face_data']
        print(d)
        # return jsonify(d)
        return d, 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        abort(400)


@app.route('/delete/person/id/<identity>', methods=['GET'])
def delete_person_by_id(identity):
    out = PersonService.PersonService.delete_person_by_id(identity)
    if out:
        return 'ok!', 200
    else:
        abort(400)


#  app.run(debug=True)
#  app.run(host='0.0.0.0') # host 0.0.0.0 makes it available over the internet
