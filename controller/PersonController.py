# router
from flask import Flask, request, Blueprint, render_template, abort, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from service import PersonService
from service.ruz import ruz
from service.weather import Weather
from validator.validator import Validator
from validator.ActiveUser import CurrentUser
from config.config import IMAGEPATH, TMP_IMAGEPATH
from playhouse.shortcuts import model_to_dict
from flasgger import Swagger
from service.nlp.VoiceAssistant import VoiceAssistant
import json
import logging
import sys

app = Flask(__name__)
Swagger(app)
app.config['JSON_AS_ASCII'] = False

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
fh = logging.FileHandler("controller.log")
formatter = logging.Formatter('%(asctime)s %(name)s :: %(levelname)s : %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.route('/get/voice/', methods=['POST'])
def get_voice():
    """Get answer via string
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: voice
        description: Person to create.
        schema:
          type: object
          properties:
            question:
              type: string
    responses:
      200:
        description: Got answer
      400:
        description: Bad JSON
    """
    file = request.get_json()
    if 'question' in file:
        return VoiceAssistant().start(file['question']), 200
    else:
        abort(400)


@app.route('/get/schedule/name/<full_name>', methods=['GET'])
def get_schedule(full_name):
    """Get JSON array of lessons for specified student by full name
    ---
    parameters:
      - name: full_name
        in: path
        type: string
        required: true
    responses:
      200:
        description: OK
      400:
        description: The full name is not in RUZ.
    """
    r = ruz.Ruz.get_schedule_by_full_name(full_name.replace('_', ' '))
    if r is not None:
        return jsonify(r), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        abort(400)


@app.route('/get/schedule/id/<identity>', methods=['GET'])
def get_schedule_by_id(identity):
    """Get JSON array of lessons for specified student by id
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: OK
          400:
            description: Specified id does not exist
        """
    person = PersonService.PersonService.get_person_by_id(identity)
    r = jsonify(ruz.Ruz.get_schedule_by_names(person.last_name,
                                              person.first_name,
                                              person.patronymic))
    if r is not None:
        return jsonify(r), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        abort(400)


@app.route('/get/weather', methods=['GET'])
def get_weather():
    """Get JSON of current weather
            ---
            responses:
              200:
                description: OK
              400:
                description: something is really, really wrong
            """
    return Weather.Weather.get_weather(), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/get/weather_date/<date>', methods=['GET'])
def get_weather_date(date):
    out = Weather.Weather.get_weather_date(date=date), 200, {'Content-Type': 'application/json; charset=utf-8'}
    if out is not None:
        return out, 200, {'Content-Type': 'application/json; charset=utf-8'}
    abort(400)


@app.route('/add/person', methods=['POST'])
def add_person():
    """Add a person via JSON POST
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: person
        description: Person to create.
        schema:
          type: object
          required:
            - last_name
            - first_name
            - patronymic
            - position
            - face_data
          properties:
            last_name:
              type: string
            first_name:
              type: string
            patronymic:
              type: string
            position:
              type: string
            mail:
              type: string
            face_data:
              type: string
              format: byte
    responses:
      200:
        description: Created
      400:
        description: Bad JSON
      420:
        description: Bad face
    """
    file = request.get_json()
    if type(file) == str:
        file = json.loads(file)
    logger.info("JSON at /add/person")
    logger.info("Type: " + str(type(file)))
    # logger.debug(file)  # a lot of lag due to output of base64 image
    if Validator.is_valid_person(file):
        logger.info("Valid JSON")
        if PersonService.PersonService.create_face(file):
            logger.info("Sucessfully added person")
            return 'ok!', 200
        else:
            logger.info("Could not create person, bad face")
            return 'bad face', 420
    else:
        logger.info("Bad JSON")
        return 'bad JSON', 400


@app.route('/add/active_user/', methods=['POST'])
def add_active_user():
    """Add or change active user
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: face
        type: file
        description: Face image
    responses:
      200:
        description: Added active user
      400:
        description: There is no such face in database / Bad face
    """
    image = request.files['face']
    if Validator.is_image(image.stream):
        CurrentUser.update(image)
        if CurrentUser.id is not None:
            return 'ok!', 200
    abort(400)


@app.route('/get/active_user', methods=['GET'])
def get_active_user():
    """Get JSON of active user
                ---
                responses:
                  200:
                    description: OK
                  400:
                    description: No active user
                """
    if CurrentUser.id is not None:
        out = PersonService.PersonService.get_person_by_id(CurrentUser.id)
        if out is not None:
            d = model_to_dict(out)
            del d['face_data']
            del d['filename']
            print(d)
            # return jsonify(d)
            return d, 200, {'Content-Type': 'application/json; charset=utf-8'}
    abort(400)


@app.route('/get/active_user/schedule', methods=['GET'])
def get_active_user_schedule():
    """Get schedule of active user
                ---
                responses:
                  200:
                    description: OK
                  400:
                    description: No active user
                """
    if CurrentUser:
        return jsonify(CurrentUser.get_schedule()), 200
    else:
        abort(400)


@app.route('/update/active_user/id/<identity>')
def update_active_user_id(identity):
    """Update active user by id
        ---
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: OK
          400:
            description: Specified id does not exist
        """
    out = CurrentUser.update_by_id(identity)
    if out is not None:
        return out
    else:
        abort(400)


@app.route('/get/person/face/', methods=['POST'])
def get_person_by_face_no_base():
    """Get person by face image
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: face
        type: file
        description: Face image
    responses:
      200:
        description: Added active user
      400:
        description: There is no such face in database / Bad face
    """
    # if request.method == 'POST':
    image = request.files['face']  # .read()
    print(image.filename)
    if Validator.is_image(image.stream):  # Validator.is_valid_filename(image.filename)
        image.save(TMP_IMAGEPATH + secure_filename(image.filename))
        out = PersonService.PersonService.find_face(
            # FaceService.FaceService.save_byte_image(image)
            TMP_IMAGEPATH + secure_filename(image.filename)
        )
        if out is not None:
            d = model_to_dict(out)
            del d['face_data']
            del d['filename']
            print(d)
            # return jsonify(d)
            return d, 200, {'Content-Type': 'application/json; charset=utf-8'}

    # evil option!
    # return redirect(url_for(get_person_by_face_no_base()))
    abort(400)
    # return render_template('face.html')


@app.route('/get/person/face/debug/', methods=['GET', 'POST'])
def debug_face():
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
                del d['filename']
                print(d)
                # return jsonify(d)
                return d, 200, {'Content-Type': 'application/json; charset=utf-8'}

        # evil option!
        # return redirect(url_for(get_person_by_face_no_base()))
        abort(400)
    return render_template('face.html')


@app.route('/get/person/id/<identity>', methods=['GET'])
def get_person_by_id(identity):
    """Get person by ID:
    ---
    parameters:
      - name: identity
        in: path
        type: integer
        required: true
    responses:
      200:
        description: OK
      400:
        description: There is no such ID
    """
    out = PersonService.PersonService.get_person_by_id(identity)
    if out is not None:
        d = model_to_dict(out)
        del d['face_data']
        del d['filename']
        print(d)
        # return jsonify(d)
        return d, 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        abort(400)


@app.route('/delete/person/id/<identity>', methods=['GET'])
def delete_person_by_id(identity):
    """Delete person by ID:
    ---
    parameters:
      - name: identity
        in: path
        type: integer
        required: true
    responses:
      200:
        description: OK
      400:
        description: There is no such ID
    """
    out = PersonService.PersonService.delete_person_by_id(identity)
    if out:
        return 'ok!', 200
    else:
        abort(400)


#  app.run(debug=True)
#  app.run(host='0.0.0.0') # host 0.0.0.0 makes it available over the internet
