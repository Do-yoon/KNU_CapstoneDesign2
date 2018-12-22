# -- coding: utf-8 --

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import json
import traceback
import sys


mysql = MySQL()
app = Flask(__name__)
api = Api(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'food'
''' add your DB username and password '''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
mysql.init_app(app)

class List(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('gate', type=str)
			args = parser.parse_args()

			_gate = args['gate']

			if _gate != 'n' and _gate != 's':
				return {'error': 'not support gate'}

			conn = mysql.connect()
			cursor = conn.cursor()
			sql = "select f_n, num, site, menu, type from {}"
			cursor.execute(sql.format(_gate))
			rows = cursor.fetchall()
			conn.close()

			payload = []
			content = {}
			for row in rows:
				content = {'f_n': row[0], 'num': row[1], 'site': row[2], 'menu': row[3], 'type': row[4]}
				payload.append(content)
				content = {}

			return json.dumps({'items': payload})

		except Exception as e:
			return {'error': str(e)}

api.add_resource(List, '/list')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

