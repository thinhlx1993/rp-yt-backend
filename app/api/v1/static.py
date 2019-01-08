from flask import Blueprint, send_file, render_template
from app.model import Mac, Agent, Email, FakeUser
from app.extensions import db
api = Blueprint('static', __name__)


@api.route('', methods=['GET'])
def serve():
    return render_template('index.html')


@api.route('<path:path>')
def static_file(path):
    return api.send_static_file(path)


# @api.route('sync_file', methods=['GET'])
# def sync():
#
#     for item in all_agemts:
#         new_agent = FakeUser()
#         new_agent.name = item['name']
#         new_agent.country = item['country']
#         new_agent.gender = item['gender']
#         new_agent.state = item['state']
#         new_agent.address_1 = item['address_1']
#         new_agent.address_2 = item['address_2']
#         new_agent.city = item['city']
#         new_agent.zip_code = item['zip_code']
#         new_agent.phone = item['phone']
#         db.session.add(new_agent)
#     db.session.commit()
#     return 'success'
