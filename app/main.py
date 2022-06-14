from flask import Flask, render_template, request
# import sys
# var = sys.path.append('..\use-cases')
import pymysql
import secrets

# conn = "mysql+pymysql://{0}:(1)0(2)/(3)".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbr


app = Flask(__name__, template_folder='../templates', static_folder='../static')
from random import randint

@app.route("/")
def index():
    return render_template("signup.html")

@app.route("/convert-currency")
def convert():
    return render_template("convert.html")

@app.route("/transfer-money")
def transfer():
    return render_template("transfer-money.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")    

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/health")
def health():
    return render_template("index.html")

@app.route("/v1/")
def home():
    return {
      "data":{
        "status":"ok",
        "message":"Welcome to the home page"
      }
    }

@app.route("/v1/currencies")
def currencies():
    return {
      "data":{
        "status":"ok",
        "message":"Welcome to the home page"
      }
    }

@app.route("/prediction", methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        income = int(request.form["income"])
        limit =  randint(0,20)/100 * income 
        return render_template("prediction.html", n = limit)
       
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return {
  "status" : 404,
  "message" : "Page not found"
}

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	 return {
  "status" : 500,
  "message" : "Internal server errror"
}

if __name__ == "__main__":
    app.run(debug=True)   