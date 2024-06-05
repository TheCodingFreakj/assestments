
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(255), nullable=False)
    age  = db.Column(db.Integer, nullable=False)
    dept = db.Column(db.String(255),nullable=False)