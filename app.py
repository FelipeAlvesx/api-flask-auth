from flask import Flask, request, jsonify
from secret import SECRET_KEY
from models.users import User
from database import db
from login_meneger_file import login_manager
from flask_login import login_user

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/hello-wolrd", methods=["GET"])
def hello_world():
    return "HELLO WORLD"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 
    
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user) # authentication
            return jsonify({"message": "login successfuly"})
    
    return jsonify({"message": "invalid credentials"}), 400


if __name__ == "__main__":
    app.run(
        debug=True
    )