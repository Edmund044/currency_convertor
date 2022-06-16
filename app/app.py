from flask import Flask, jsonify, render_template, request, url_for, redirect
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint


def make_request_to_convert_currency(amount1,  currency1, currency2):
    url = "https://api.apilayer.com/fixer/convert?to=" + \
        currency2+"&from="+currency1+"&amount="+amount1

    payload = {}
    headers = {
        "apikey": "Slyih31Y8eUs3dRJgZyPjaPCzVh8s01y"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    res = json.loads(response.text)

    return res


app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currency_convertor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    picture = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(5), nullable=False)
    wallet_number = db.Column(db.Integer, nullable=False)
    wallet_balance = db.Column(db.Float(20), nullable=False)


@app.route("/")
def index():
    return render_template("signup.html")


@app.route("/convert-currency")
def convert():
    return render_template("convert.html")


@app.route("/transfer-money")
def transfer():
    return render_template("transfer.html")


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
    try:
        if request.method == "POST":
            first_name = request.form["first_name"]
            second_name = request.form["second_name"]
            currency = request.form["currency"]
            email = request.form["email"]
            picture = "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]
            wallet_number = randint(123545224, 873648754)
            if password != confirm_password:
                return "Passwords do not match"
            user = User.query.filter_by(email=email).first()
            if user:
                return "User already exists"
            else:
                response = make_request_to_convert_currency(
                    "1000", "USD", currency)
            wallet_balance = response["result"]
            new_user = User(first_name=first_name, second_name=second_name, currency=currency, email=email, picture=picture, wallet_number=wallet_number, wallet_balance=wallet_balance,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("signin"))
    except:
        return redirect(url_for("signin"))


@app.route("/handle-signin", methods=["POST"])
def handle_signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return redirect(url_for("convert"))
            else:
                return "Password is incorrect"
        else:
            return "User does not exist"


@app.route("/get_transaction", methods=["POST"])
def get_transaction():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    return render_template("dashboard.html")


@app.route("/handle-profile-update", methods=["POST"])
def handle_profile_update():
    if request.method == "POST":
        first_name = request.form["first_name"]
        second_name = request.form["second_name"]
        currency = request.form["currency"]
        email = request.form["email"]
        picture = request.form["picture"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

    return render_template("dashboard.html")


@app.route("/handle-convert-currency", methods=["POST"])
def handle_convert_currency():
    if request.method == "POST":
        amount1 = request.form["amount1"]
        currency1 = request.form["currency1"]
        currency2 = request.form["currency2"]

    response = make_request_to_convert_currency(amount1, currency1, currency2)
    return render_template("converted-currency.html", amount1=amount1, amount2=response["result"], currency1=currency1, currency2=currency2)


@app.route("/handle-transfer-money", methods=["POST"])
def handle_transfer_money():
    transaction_rate_fee = 0.05
    wallet_balance = 10000
    amount_to_send = 0
    wallet_number = 0
    sender_currency = "USD"
    receiver_currency = "NGN"
    amount_to_receive = 0
    rate = 0.89
    if request.method == "POST":
        amount_to_send = request.form["amount_to_send"]
        wallet_number = request.form["wallet_number"]
    # make sure wallets exists
    if float(amount_to_send) + float(amount_to_send) * transaction_rate_fee < wallet_balance:
        transfer_status = "Succesful transfer"
        transaction_cost = float(amount_to_send) * transaction_rate_fee
        amount_to_receive = float(amount_to_send) * rate
        new_balance = float(wallet_balance) - (float(amount_to_send) +
                                               float(amount_to_send) * transaction_rate_fee)
        # update sender wallet
        # update receiver wallet

    elif float(amount_to_send) + float(amount_to_send) * transaction_rate_fee > wallet_balance:
        transfer_status = "Insufficient funds"
        transaction_cost = 0
        amount_to_receive = 0
        new_balance = wallet_balance
    else:
        transfer_status = "Failed transfer"
        transaction_cost = 0
        new_balance = wallet_balance

    return render_template("transfered-money.html", amount_to_receive=amount_to_receive, wallet_number=wallet_number, transfer_status=transfer_status, sender_currency=sender_currency, receiver_currency=receiver_currency, new_balance=new_balance, transaction_cost=transaction_cost)


@app.route("/health")
def health():
    return {
        "data": {
            "status": "ok",
            "message": "API is up and running"
        }
    }


@app.route("/v1/")
def home():
    return {
        "data": {
            "status": "ok",
            "message": "Welcome to the home page"
        }
    }


@app.route("/v1/currencies")
def currencies():
    return {
        "data": {
            "status": "ok",
            "message": "Welcome to the home page"
        }
    }


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return {
        "status": 404,
        "message": "Page not found"
    }

# Internal Server Error


@app.errorhandler(500)
def page_not_found(e):
    return {
        "status": 500,
        "message": "Internal server errror"
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)