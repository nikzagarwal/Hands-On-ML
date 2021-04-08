from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import random


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'
app.config['SQLALCHEMY_BINDS']={'datadb':'sqlite:///data.db','trainedmodeldb':'sqlite:///trainedmodel.db','projectinfodb':'sqlite:///projectinfo.db','projectsdb':'sqlite:///projects.db'}

db=SQLAlchemy(app)

class UserDB(db.Model):
	userID=db.Column(db.Integer,primary_key=True,nullable=False)
	username=db.Column(db.String(150),nullable=False)
	password=db.Column(db.String(150),nullable=False)
	def __init__(self,userID,username,password):
		self.userID=userID
		self.username=username
		self.password=password

class ProjectInfoDB(db.Model):
	__bind_key__='projectinfodb'
	projectUserID=db.Column(db.Integer,primary_key=True,nullable=False)
	userID=db.Column(db.Integer,nullable=False)
	def __init__(self,projectUserID,userID):
		self.projectUserID=projectUserID
		self.userID=userID
	
class ProjectsDB(db.Model):
	__bind_key__='projectsdb'
	projectID=db.Column(db.Integer,primary_key=True,nullable=False)
	dataID=db.Column(db.Integer,nullable=False)
	projectname=db.Column(db.String(100))
	projectdata=db.Column(db.PickleType)			#This is PickleType Can be useful
	def __init__(self,projectID,dataID,projectname,projectdata):
		self.projectID=projectID
		self.dataID=dataID
		self.projectname=projectname
		self.projectdata=projectdata	

class TrainedModelsDB(db.Model):
	__bind_key__='trainedmodeldb'
	modelname=db.Column(db.String(100),primary_key=True,nullable=False)
	parameters=db.Column(db.String(100),nullable=False)
	weights=db.Column(db.String(100))
	metrics=db.Column(db.String(100))
	def __init__(self,modelname,parameters,weights,metrics):
		self.modelname=modelname
		self.parameters=parameters
		self.weights=weights
		self.metrics=metrics

class DataDB(db.Model):
	__bind_key__='datadb'
	dataID=db.Column(db.String(100),primary_key=True,nullable=False)
	traineddata=db.Column(db.PickleType,nullable=False)
	validationdata=db.Column(db.PickleType)
	def __init__(self,dataID,traineddata,validationdata):
		self.dataID=dataID
		self.traineddata=traineddata
		self.validationdata=validationdata
db.create_all()

myUserObject=UserDB(15,"UserTheGreat","PasswordTheStrong")
myMLObject=TrainedModelsDB("KNN","Params","Weights","Metrics")
	
@app.route("/")
def myfunction():
	return render_template("index.html",myUserObject=myUserObject,myMLObject=myMLObject)

@app.route("/update",methods=["POST"])
def myDBfunction():
	mycurrentuser=UserDB.query.get_or_404(myUserObject.userID)
	if request.method=='POST':
		try:
			db.session.commit(trainedmodeldb)
			return redirect('/')
		except:
			return 'There was an error updating that task'
	else:
		return render_template('index.html',myMLObject=myMLObject,myUserObject=myUserObject)


if __name__=='__main__':
	app.run(debug=True)
