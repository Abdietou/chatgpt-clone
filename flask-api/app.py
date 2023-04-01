from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# create an instance of flask
app = Flask(__name__)

CORS(app)

# creating an API object
api = Api(app)

CORS(app, origins='http://localhost:8080')

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#sqlalchemy mapper
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.content}"

# For GET request to http://localhost:5000/
class GetHistory(Resource):
    def get(self):
        history = History.query.all()
        hist_list = []
        for hist in history:
            hist_data = {'Id': hist.id, 'Content': hist.content}
            hist_list.append(hist_data)
        return {"history": hist_list}, 200

# For Post request to http://localhost:5000/add
class AddHistory(Resource):
    def post(self):
        if request.is_json:
            hist = History(content=request.json['Content'])
            db.session.add(hist)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'Id': hist.id, 'Content': hist.content}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# For put request to http://localhost:5000/update/id
class UpdateHistory(Resource):
    def put(self, id):
        if request.is_json:
            hist = History.query.get(id)
            if hist is None:
                return {'error': f'History with id {id} not found'}, 404
            else:
                hist.content = request.json['Content']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/delete/id
class DeleteHistory(Resource):
    def delete(self, id):
        hist = History.query.get(id)
        if hist is None:
            return {'error': f'History with id {id} not found'}, 404
        db.session.delete(hist)
        db.session.commit()
        return f'History with id {id} is deleted', 200


api.add_resource(GetHistory, '/')
api.add_resource(AddHistory, '/add')
api.add_resource(UpdateHistory, '/update/<int:id>')
api.add_resource(DeleteHistory, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)