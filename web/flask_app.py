from flask import Flask

app = Flask(__name__)
# app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"