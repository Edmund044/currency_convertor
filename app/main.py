from flask import Flask, render_template, request, url_for


app = Flask(__name__, template_folder='../templates', static_folder='../static')


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

@app.route("/handle-signup", methods=["POST"])
def handle_signup():
    if request.method == "POST":
          first_name = request.form["first_name"]
          second_name = request.form["second_name"]
          currency = request.form["currency"]
          email =  request.form["email"]
          picture = request.form["picture"]
          password =  request.form["password"]
          confirm_password = request.form["confirm_password"]

    return render_template("dashboard.html")

@app.route("/handle-signin", methods=["POST"])
def handle_signin():
    if request.method == "POST":
          email =  request.form["email"]
          password =  request.form["password"] 

    return render_template("dashboard.html")  

@app.route("/get_transaction", methods=["POST"])
def get_transaction():
    if request.method == "POST":
          email =  request.form["email"]
          password =  request.form["password"] 

    return render_template("dashboard.html")    


@app.route("/handle-profile-update", methods=["POST"])
def handle_profile_update():
    if request.method == "POST":
          first_name = request.form["first_name"]
          second_name = request.form["second_name"]
          currency = request.form["currency"]
          email =  request.form["email"]
          picture = request.form["picture"]
          password =  request.form["password"]
          confirm_password = request.form["confirm_password"]

    return render_template("dashboard.html")

@app.route("/handle-convert-currency", methods=["POST"])
def handle_convert_currency():
    if request.method == "POST":
          amount1 =  request.form["amount1"]
          currency1 = request.form["currency1"] 
          amount2 =  request.form["amount2"]
          currency2 = request.form["currency2"]       
          
    return render_template("dashboard.html") 

@app.route("/handle-transfer-money", methods=["POST"])
def handle_transfer_money():
    if request.method == "POST":
          amount_to_send =  request.form["amount_to_send"]
          wallet_number = request.form["wallet_number"]      
          
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
      app.run(host='0.0.0.0', debug=True)  
   