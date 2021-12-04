from app import db
import time
import uuid
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(500), primary_key = True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    email = db.Column(db.String(255), unique=True)
    message = db.Column(db.String(1000),default="Happy birthday! I hope all your birthday wishes and dreams come true")
    # userSignIn = db.Column(db.String(255), unique=True)

    def __init__(self, name, email,phone,dob,message="Happy Birthday!!! I hope all your birthday wishes and dreams come true"):
        self.id = round(time.time() * 1000)
        self.name = name
        self.email = email
        self.phone = phone
        self.dob = dob
        self.message = message

    def __repr__(self):
        print(self.id)
        print(self.name)
        print(self.email)
        print(self.phone)
        print(self.dob)
        print(self.message)
        return '<User %r>' % self.name

