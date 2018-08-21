from flask import Blueprint, send_file, render_template

api = Blueprint('static', __name__)


@api.route('', methods=['GET'])
def serve():
    return render_template('index.html')


@api.route('<path:path>')
def static_file(path):
    return api.send_static_file(path)
