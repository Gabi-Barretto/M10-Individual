from flask import Flask, jsonify, make_response, request, render_template
import requests as http_request
from database.database import db
from database.models import User
from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from flasgger import Swagger, swag_from

app = Flask(__name__, template_folder="templates")

CORS(app, origins=["http://127.0.0.1:5000/token"], supports_credentials=True)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

# Create Database (if specified)
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    with app.app_context():
        db.create_all()
    print("Database created successfully")
    sys.exit(0)

# Configure Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)

# Routes
@app.route("/")
def hello_world():
    return "Hello, World!" 

@app.route("/register", methods=["POST"])
@swag_from("yamls/register.yaml")
def register_user():
    data = request.form
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# User CRUD Routes
@app.route("/users", methods=["GET"])
@swag_from("yamls/get-users.yaml")
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
@swag_from("yamls/get-user-by-id.yaml")
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<int:id>", methods=["PUT"])
@swag_from("yamls/update-user.yaml")
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if user:
        user.name = data["name"]
        user.email = data["email"]
        user.password = data["password"]
        db.session.commit()
        return jsonify(user.serialize())
    else: 
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<int:id>", methods=["DELETE"])
@swag_from("yamls/delete-user.yaml")
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.serialize())
    else:
        return jsonify({"message": "User not found"}), 404 
    
@app.route("/login", methods=["POST"])
@swag_from("yamls/login.yaml")
def login():
    username = request.form.get("email", None)
    password = request.form.get("password", None)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"email": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    # recupera o token
    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response

# Auth Routes
@app.route("/user-login", methods=["GET"])
@swag_from("yamls/user-login.yaml")
def user_login():
    return render_template("login.html")

@app.route("/user-register", methods=["GET"])
@swag_from("yamls/user-register.yaml")
def user_register():
    return render_template("register.html") 

@app.route("/content", methods=["GET"])
@jwt_required()
@swag_from("yamls/content.yaml")
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
@swag_from("yamls/error.yaml")
def error():
    return render_template("error.html")

@app.route("/token", methods=["POST"])
@swag_from("yamls/create-token.yaml") 
def create_token():
    username = request.json.get("email", None) 
    password = request.json.get("password", None)
    user = User.query.filter_by(email=username, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id": user.id}) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)