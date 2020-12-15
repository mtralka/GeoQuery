from app import create_app
from app import db


db.create_all(app=create_app())
print("Model Created")
