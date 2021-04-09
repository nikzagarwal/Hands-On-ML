from flask import Flask, render_template , request, url_for
from preprocess import *
from flask_sqlalchemy import SQLAlchemy
from random import randint

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)



class Project(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    dataid=db.relationship('Data',backref='nameid')


class Data(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dftrain= db.Column(db.String(50),nullable=False)
    ytrain=db.Column(db.String(50),nullable=False)
    dftest=db.Column(db.String(50),nullable=False)
    ytest=db.Column(db.String(50),nullable=False)
    owner_id=db.Column(db.Integer,db.ForeignKey('project.sno'))
   


@app.route('/')
def home():       
   urldata=url_for('static', filename='cardata.csv')
   return render_template('create.html')

@app.route('/create')
def create():       
   return render_template('create.html')


@app.route('/clean',methods=['GET','POST'])
def clean():
    if request.method=='POST':
      name=request.form['name']
      train=request.form['train']
      urldata=url_for('static', filename='cardata.csv')
      return render_template('data.html',urldata=urldata)

       
@app.route('/data',methods=['GET','POST'])
def data():
   if request.method=='POST':
      prono=str(randint(0,99999999))
      x=Project(name=idi)
      db.session.add(x)
      db.session.commit()
      cols=request.form['colno']
      # rows=request.form['rowno']
      changetype=request.form['encodetype']
      encodecol=request.form['encode']
      scaling=request.form['scaletype']
      scalingcol=request.form['scale']
      targetcol=request.form['target']
      clean(cols=cols,rows="",changetype=changetype,encodecol=encodecol,scaling=scaling,scalingcol=scalingcol,targetcol=targetcol,dftest="",sno=prono)
      path="/static/data/"+prono
      newfile=Data(dftrain=path+"/dftrain.csv",ytrain=path+"/ytrain.csv",dftest=path+"/dftest.csv",ytest=path+"/ytest.csv",nameid=x)
      db.session.add(newfile)
      db.session.commit()
      return render_template('model.html',newfile=newfile)



if __name__ == '__main__':
   app.run(debug=True )