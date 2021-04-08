from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///testdb.sqlite3'
db=SQLAlchemy(app)

class MLModels(db.Model):
	serialNumber=db.Column(db.Integer,primary_key=True)
	modelname=db.Column(db.String(150),nullable=False)
	modelparams=db.Column(db.String(300),nullable=True)
	modelmetrics=db.Column(db.String(300),nullable=True)
	def __init__(self,serialNumber,modelname,modelparams,modelmetrics):
		self.serialNumber=serialNumber
		self.modelname=modelname
		self.modelparams=modelparams
		self.modelmetrics=modelmetrics
		

db.create_all()


@app.route("/")
def myfunction():
	myMLobject=MLModels(1,"KNN","Params","Metrics")
	return render_template("index.html",myMLobject=myMLobject)


if __name__=='__main__':
	app.run(debug=True)
