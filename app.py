'''
from flask import Flask
from example_blueprint import example_blueprint

app = Flask(__name__)
app.register_blueprint(example_blueprint)
'''

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource,reqparse
import hypothesis
import json

flask_app = Flask(__name__)
app = Api(app = flask_app, version='1.0', title='Tagging all document with hypothesis', description='You can tag any document', default ='Test', default_label='Yo can try it!')

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
	def post(self, url_doc, words, user):
		words=words.split(', ')
		print('->',words)
		hy=hypothesis.main(url_doc, words)
		print('https://hypothes.is/users/'+user)
		return ('https://hypothes.is/users/'+user)


class Todo2(Resource):
	def get(self):
		ids=hypothesis.search_annotation()

		return jsonify(ids[1])

class Todo3(Resource):
	def post(self, delete):
		ids=delete.split(', ')
		print('->',ids)
		hy=hypothesis.delete_annotation(ids)
		
		return jsonify(hy)
		

app.add_resource(Todo, '/<string:url_doc>/<string:words>/<string:user>')
app.add_resource(Todo2, '/search')
app.add_resource(Todo3, '/<string:delete>')

