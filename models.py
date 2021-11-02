from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    message = db.Column(db.String(1000),default="Happy birthday! I hope all your birthday wishes and dreams come true")

    def __init__(self,id, name, email,message="Happy Birthday!!! I hope all your birthday wishes and dreams come true"):
        self.id = id
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        print(self.id)
        print(self.name)
        print(self.email)
        print(self.message)
        return '<User %r>' % self.name

