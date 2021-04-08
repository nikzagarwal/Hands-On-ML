from flask import Flask, render_template
import requests
import random

app=Flask(__name__)


@app.route("/")
def myfunction():
	return render_template("index.html",myvariable=myvariable)


if __name__=='__main__':
	app.run(debug=True)
	
