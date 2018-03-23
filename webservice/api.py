import pymongo
from flask import Flask,request,jsonify,url_for,redirect 
from flask_restful import Resource ,Api ,reqparse
import json
from bson import ObjectId


client = pymongo.MongoClient('localhost',27017)

app= Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
	return response

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('artist')


db = client.db_listOfmusic

music = db.music
class Musics(Resource):
        def get(self):
		args = parser.parse_args()
            	id = args['id']
		items = []
		if id:
			data = music.find_one({"_id":ObjectId(id)})
			if data:
				return {"id":str(data['_id']),"name":data['name'],"artist":data['artist']}
			return {}

		#{"_id":ObjectId('5ab3484ad4fbbf0e3fce0d45')}
		data = music.find()
		print (data)
		if data:
			for item in data:
				id = str(item.get("_id"))
				print (id)
				items.append({"id":id,"name":item['name'],"artist":item['artist']})
			return jsonify({"data":items})
		return {}
	def post(self):
		args = parser.parse_args()
		name = args['name']
		artist = args['artist']
		if(name and artist):
			music.insert({"name":name,"artist":artist})
			return {"name":name,"artist":artist}
		return {"err":"data empty"}
	def patch(self):
		args = parser.parse_args()
		id = args['id']
		name = args['name']
		artist = args['artist']
		if(id and name and artist):
			music.update({"_id":ObjectId(id)},{"name":name,"artist":artist})
		return {}
	def delete(self):
		args = parser.parse_args()
		id = args['id']
		if(id):
			music.remove({"_id":ObjectId(id)})
		return {}

api.add_resource(Musics,'/api/musics')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5000)
