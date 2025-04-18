from flask import Flask, request, jsonify
from secret import SECRET_KEY
from models.users import User
from database import db
from login_meneger_file import login_manager
from flask_login import login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login' # View login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 
    
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user) # authentication
            print(current_user.is_authenticated)
            return jsonify({"message": "login successfuly"})
    
    return jsonify({"message": "invalid credentials"}), 400


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if email and password:
        user = User(username=username, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "create"})

    return jsonify({"message": "invalid credentials"}), 400



@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def get_user(id_user):
    user = User.query.get(id_user)

    if user:
        user = User.query.get(id_user)

        if user.username and user.email and user.password:
            return jsonify({"username": user.username, "email": user.email})
        
        elif user.username and user.password:
            return jsonify({"username": user.username})
        
        elif user.email and user.password:
            return jsonify({"email": user.email})
        

    return jsonify({"message": "not found"}), 404



@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    password = data.get("password")
    username = data.get("username") 
    user = User.query.get(id_user)
    # CURRENT USER

    if data.get("email"):
        return jsonify({"message": "email cannot be changed"}), 403
    

    if user and (password or username):
        if username:
            user.username = username
        if password:
            user.password = password
            user.set_password(password)
            
        db.session.commit()

        
        return jsonify({"message": f"update user succesfuly - ID {id_user}"})
             

    return jsonify({"message": "not found"}), 404


@app.route("/user/<int:id_user>", methods=["DELETE"])
def delete_user(id_user):
    user = User.query.get(id_user)
    
    if id_user == current_user.id:
        return jsonify({"message": "logged in users cannot be deleted"}), 403
    if user:
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"user deleted ID - {id_user}"})

    return jsonify({"message": "not found"}), 404

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfuly"})



if __name__ == "__main__":
    app.run(
        debug=True
    )