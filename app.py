from flask import Flask, request
from secret import SECRET_KEY
from models.users import User
from database import db
from login_meneger_file import login_manager

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if email and password:
        ...

if __name__ == "__main__":
    app.run(
        debug=True
    )