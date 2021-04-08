from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


class MLModelsDB(db.Model):
	serialNumber=db.Column(db.Integer,primary_key=True)
	modelname=db.Column(db.String(150),nullable=False)
	modelparams=db.Column(db.String(300),nullable=True)
	modelmetrics=db.Column(db.String(300),nullable=True)
	def __init__(self,serialNumber,modelname,modelparams,modelmetrics):
		self.serialNumber=serialNumber
		self.modelname=modelname
		self.modelparams=modelparams
		self.modelmetrics=modelmetrics
		
class UsersDB(db.Model):
	username=db.Column(db.String(150),primary_key=True)
	password=db.Column(db.String(150),nullable=False)
	def __init__(self,username,password):
		self.username=username
		self.password=password
