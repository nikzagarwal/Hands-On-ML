from flask import Flask, render_template , request, url_for ,session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from random import randint
import os
import json

with open('templates/config.json','r') as c:
   params = json.load(c)["params"]

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = params['server']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.secret_key = params['key']      

class Login(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    user=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)

class Project(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    rawdata=db.Column(db.String(50))
    cleandata=db.Column(db.String(50))
    common=db.Column(db.Integer,nullable=False)
    user=db.Column(db.Integer,nullable=False)

class Data(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dftrain= db.Column(db.String(50),nullable=False)
    ytrain=db.Column(db.String(50),nullable=False)
    dftest=db.Column(db.String(50),nullable=False)
    ytest=db.Column(db.String(50),nullable=False)
    common=db.Column(db.Integer,nullable=False)

class Modeldb(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    modelType= db.Column(db.String(50))
    modelName= db.Column(db.String(50))
    weights=db.Column(db.String(50))
    metricsid=db.relationship('Metricdb',backref='metricsid')
    common=db.Column(db.Integer,nullable=False)

class Metricdb(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    accuracy=db.Column(db.String(50))
    f1score=db.Column(db.String(50))
    precision=db.Column(db.String(50))
    recall=db.Column(db.String(50))
    rmse=db.Column(db.String(50))
    r2=db.Column(db.String(50))
    owner_id=db.Column(db.Integer,db.ForeignKey('modeldb.sno'))
    common=db.Column(db.Integer,nullable=False)

@app.route("/logout")
def logout():
    session.pop('user',None)
    return render_template('login.html')

@app.route("/newuser",methods=['GET','POST'])
def new():
   if request.method=='POST':
      name=request.form['name']
      username=request.form['user']
      password=request.form['passw']
      x=Login(name=name,user=username,password=password)
      db.session.add(x)
      db.session.commit()
      return render_template('Login.html')
   return render_template('newuser.html')

@app.route('/')
def home():  
   if('user' in session):    
         return render_template('index.html')
   return render_template('login.html')


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():   
   if request.method=='POST':
      username=request.form['user']
      password=request.form['passw']
      allusers=Login.query.all()
      for i in allusers:
         if i.user==username and i.password == password:
            session['user']=username
            session['sno']=i.sno
            return render_template('index.html')
      return render_template('login.html')      

@app.route('/create',methods=['GET','POST'])
def create():
      return render_template('create.html')
from getoption import*
@app.route('/clean',methods=['GET','POST'])
def clean():
    if request.method=='POST':
      name=request.form['name']
      train=request.files['train']
      test=request.files['test']
      cleandatapath="static/data/"+str(randint(0,9999999999))
      os.mkdir(cleandatapath)
      cleandatapath+="/"
      session['cleandatapath'] = cleandatapath
      rawdatapath="static/rawdata/"+str(randint(0,9999999999))
      os.mkdir(rawdatapath)
      rawdatapath+='/'
      train.save(rawdatapath+train.filename)
      rawdatapath+=train.filename
      session['rawdatapath'] = rawdatapath
      num= randint(0,9999999999)
      session['num'] = num
      sno= session.get('sno', None)
      x=Project(name=name, rawdata=rawdatapath,cleandata=cleandatapath,common=num,user=sno)
      db.session.add(x)
      db.session.commit()
      session['train'] = train.filename
      option=getoptionpy(rawdatapath)
      print(option)
      return render_template('data2.html',urldata=rawdatapath,x=x,option=option)

from preprocess import*
from preprocess2 import*
from makemodel import*


@app.route('/data',methods=['GET','POST'])
def data():
   if request.method=='POST':
      num= session.get('num', None)
      cleandatapath= session.get('cleandatapath', None)
      rawdatapath= session.get('rawdatapath', None)
      cols=request.form.getlist('colno')
      changetype=request.form['encodetype']
      encodecol=request.form.getlist('encode')
      scaling=request.form['scaletype']
      scalingcol=request.form.getlist('scale')
      targetcol=request.form['target']
      cleanpy2(cols=cols,changetype=changetype,encodecol=encodecol,scaling=scaling,scalingcol=scalingcol,targetcol=targetcol,dftest="",cleandatapath=cleandatapath,rawdatapath=rawdatapath)
      path=cleandatapath
      dftrainpath=path+"dftrain.csv"
      dftestpath=path+"dftest.csv"
      ytrainpath=path+"ytrain.csv"
      ytestpath=path+"ytest.csv"
      session['dftrainpath'] = dftrainpath
      session['dftestpath'] = dftestpath
      session['ytrainpath'] = ytrainpath
      session['ytestpath'] = ytestpath
      c=0
      sno=0
      alldata=Data.query.all()
      for i in alldata:
            if i.common==num:
               c+=1
               sno=i.sno
               x=Data.query.get(sno)
               return render_template('model2.html',newfile=x)
      if(c==0):      
         newfile=Data(dftrain=path+"dftrain.csv",ytrain=path+"ytrain.csv",dftest=path+"dftest.csv",ytest=path+"ytest.csv",common=num)
         db.session.add(newfile)
         db.session.commit()
         return render_template('model2.html',newfile=newfile)

@app.route('/metrics',methods=['GET','POST'])
def metrics():
   if request.method=="POST":
      modeltype=request.form["mtype"]
      if(modeltype=="classification"):
         model=request.form["model1"]
      else:
         model=request.form["model2"]
      alpha=request.form["alpha"]
      if type(alpha)!=float:
         alpha=1
      n_neighbors=(request.form['n_neighbors'])
      if type(n_neighbors)!=int:
         n_neighbors=5
      leaf_size=request.form['leaf_size']
      if type(leaf_size)!=int:
         leaf_size=30
      max_depth=(request.form['max_depth'])
      if type(max_depth)!=int:
         max_depth=50
      min_samples_split=request.form['min_samples_split']
      if type(min_samples_split)!=int:
         min_samples_split=2
      n_estimators=(request.form['n_estimators'])
      if type(n_estimators)!=int:
         n_estimators=500
      random_state=request.form['random_state']
      if type(random_state)!=int:
         random_state=42
      max_leaf_nodes=request.form['max_leaf_nodes']
      if type(max_leaf_nodes)!=int:
         max_leaf_nodes=50

      dftrainpath= session.get('dftrainpath', None)
      ytrainpath= session.get('ytrainpath', None)
      dftestpath= session.get('dftestpath', None)
      ytestpath= session.get('ytestpath', None)
      num= session.get('num', None)
      x,y=output(modeltype,model,dftrainpath,ytrainpath,dftestpath,ytestpath,db,num,float(alpha),int(n_neighbors),int(leaf_size),int(max_depth),int(min_samples_split),int(n_estimators),int(random_state),int(max_leaf_nodes))
      mydata=Data.query.all()
      return render_template('metrics.html',x=x,y=y,mydata=mydata)
@app.route('/projects')
def pro():
   mypro=Project.query.all()
   mydata=Data.query.all()
   mymetric=Metricdb.query.all()
   mymodel=Modeldb.query.all()
   sno= session.get('sno', None)
   return render_template('projects.html',mypro=mypro,mydata=mydata,mymetric=mymetric,mymodel=mymodel,sno=sno)

if __name__ == '__main__':
   app.run(debug=True)