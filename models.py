from app import db
import datetime
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    email = db.Column(db.String(255), unique=True)
    message = db.Column(db.String(1000),default="Happy birthday! I hope all your birthday wishes and dreams come true")

    def __init__(self, name, email,phone,dob,message="Happy Birthday!!! I hope all your birthday wishes and dreams come true"):
        # self.id = id
        # format = '%Y-%B-%d'
        # date = datetime.strptime(dob,format)
        # datetime.strftime(datetime.strptime('15-MARCH-2015','%d-%B-%Y'),'%Y-%m-%d')

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

