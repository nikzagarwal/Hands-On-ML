from flask import Flask, render_template , request
from preprocess import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)



class Project(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dataid=db.relationship('Data',backref='owner')

class Data(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    dftrain= db.Column(db.String(50),nullable=False)
    ytrain=db.Column(db.String(50),nullable=False)
    dftest=db.Column(db.String(50),nullable=False)
    ytest=db.Column(db.String(50),nullable=False)
    owner_id=db.Column(db.Integer,db.ForeignKey('project.sno'))
   

    def __repr__(self) -> str:
        return f"{self.sno}"

@app.route('/')
def home():
   return render_template('data.html')

@app.route('/<int:sno>',methods=['GET','POST'])
def data(sno):
   if request.method=='POST':
      cols=request.form['colno']
      rows=request.form['rowno']
      changetype=request.form['encodetype']
      encodecol=request.form['encode']
      scaling=request.form['scaletype']
      scalingcol=request.form['scale']
      targetcol=request.form['target']
      clean(cols=cols,rows=rows,changetype=changetype,encodecol=encodecol,scaling=scaling,scalingcol=scalingcol,targetcol=targetcol,dftest="",db=db)
      return redirect('data.html')
   return render_template('data.html',sno=sno)



if __name__ == '__main__':
   app.run(debug=True)