from flask import Flask, request
from flask_restful import Api,Resource, reqparse,abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api=Api(app); #wrapping app in api

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db=SQLAlchemy(app);


class MyData(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),nullable=False)
	views=db.Column(db.Integer,nullable=False)
	likes=db.Column(db.Integer,nullable=False)

	def __repr__(self):
		return f"Video(name ={name},views={views},likes={likes})"



video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Name Not Found",required="True")
video_put_args.add_argument("views",type=str,help="Views Not Found",required="True")
video_put_args.add_argument("likes",type=str,help="Likes Not Found",required="True")



class WebSeries(Resource):
	def get(self,wid):
		help_get_and_delete(wid)
		return webseries[wid]


	def put(self,wid):
		help_put(wid)
		args=video_put_args.parse_args();
		webseries[wid]=args
		return webseries[wid], 201

	def delete(self, wid):
		help_get_and_delete(wid)
		return '',204

api.add_resource(WebSeries,"/series/<int:wid>")





if __name__== "__main__":
	app.run(debug=True)

