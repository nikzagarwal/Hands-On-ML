from flask import Flask, render_template , request, url_for ,session
from preprocess import *
from makemodel import*
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from random import randint
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'





class Project(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    rawdata=db.Column(db.String(50))
    cleandata=db.Column(db.String(50))

class Data(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dftrain= db.Column(db.String(50),nullable=False)
    ytrain=db.Column(db.String(50),nullable=False)
    dftest=db.Column(db.String(50),nullable=False)
    ytest=db.Column(db.String(50),nullable=False)

class Modeldb(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    modelType= db.Column(db.String(50))
    modelName= db.Column(db.String(50))
    weights=db.Column(db.String(50))
    metricsid=db.relationship('Metricdb',backref='metricsid')

class Metricdb(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    accuracy=db.Column(db.String(50))
    f1score=db.Column(db.String(50))
    precision=db.Column(db.String(50))
    recall=db.Column(db.String(50))
    rmse=db.Column(db.String(50))
    r2=db.Column(db.String(50))
    owner_id=db.Column(db.Integer,db.ForeignKey('modeldb.sno'))
    
@app.route('/')
def home():       
   return render_template('login.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():   
   if request.method=='POST':
      username=request.form['user']
      password=request.form['passw']    
      if (username=="admin" and password=="123"):
         session['user']=username
         return render_template('create.html')
      else:
         return render_template('login.html')
   else:
      return render_template('login.html')



@app.route('/create')
def create():       
   return render_template('create.html')


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
      x=Project(name=name, rawdata=rawdatapath,cleandata=cleandatapath)
      db.session.add(x)
      db.session.commit()
      session['train'] = train.filename
      # urldata=url_for('static', filename='cardata.csv')
      return render_template('data.html',urldata=rawdatapath,x=x)
     
@app.route('/data',methods=['GET','POST'])
def data():
   if request.method=='POST':
      cleandatapath= session.get('cleandatapath', None)
      rawdatapath= session.get('rawdatapath', None)
      cols=request.form['colno']
      changetype=request.form['encodetype']
      encodecol=request.form['encode']
      scaling=request.form['scaletype']
      scalingcol=request.form['scale']
      targetcol=request.form['target']
      cleanpy(cols=cols,rows="",changetype=changetype,encodecol=encodecol,scaling=scaling,scalingcol=scalingcol,targetcol=targetcol,dftest="",cleandatapath=cleandatapath,rawdatapath=rawdatapath)
      path=cleandatapath
      dftrainpath=path+"dftrain.csv"
      dftestpath=path+"dftest.csv"
      ytrainpath=path+"ytrain.csv"
      ytestpath=path+"ytest.csv"
      session['dftrainpath'] = dftrainpath
      session['dftestpath'] = dftestpath
      session['ytrainpath'] = ytrainpath
      session['ytestpath'] = ytestpath
      newfile=Data(dftrain=path+"dftrain.csv",ytrain=path+"ytrain.csv",dftest=path+"dftest.csv",ytest=path+"ytest.csv")
      
      db.session.add(newfile)
      db.session.commit()
      return render_template('model2.html',newfile=newfile)

@app.route('/metrics',methods=['GET','POST'])
def metrics():
   if request.method=="POST":
      modeltype=request.form["mtype"]
      model=request.form["model"]
      var_smoothing=request.form["var_smoothing"]
      n_neighbors=request.form['n_neighbors']
      leaf_size=request.form['leaf_size']
      max_depth=request.form['max_depth']
      min_samples_split=request.form['min_samples_split']
      n_estimators=request.form['n_estimators']
      random_state=request.form['random_state']
      max_leaf_nodes=request.form['max_leaf_nodes']

      dftrainpath= session.get('dftrainpath', None)
      ytrainpath= session.get('ytrainpath', None)
         
      x,y=output(modeltype,model,var_smoothing,n_neighbors,leaf_size,max_depth,min_samples_split,n_estimators,random_state,max_leaf_nodes,dftrainpath,ytrainpath,db)
      return render_template('metrics.html',x=x,y=y)

if __name__ == '__main__':
   app.run(debug=True )