from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime

#Initialising Flask 
app = Flask(__name__)

# #DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
import models
db.create_all()

mail = Mail(app)

#Mailer Config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'birthdaywishingbot@gmail.com'
app.config['MAIL_PASSWORD'] = 'approject2021'
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
    


# Home page route
@app.route('/')
def index():
    # Fetch all users 
    users = models.User.query.all()
    return render_template("index.html",users=users)


# Testing DB connection route
@app.route('/',methods=['POST','GET']) 
def test():
    if request.method == 'POST':    
        print(request.form)
        userName = request.form['name']
        userPhone = request.form['phone']
        userEmail = request.form['email']
        userDob = request.form['dob']
        userMessage = request.form['message']
        
        format = '%Y-%m-%d'
        date = datetime.datetime.strptime(userDob,format)
        print("date : ",date)
        print(userName,userPhone,userEmail,date,userMessage,sep=" ")
        newUser = models.User(name=userName,email=userEmail,phone=userPhone,dob=date,message=userMessage)
        print("new User : ",newUser)
        try:
            print(db)
            print(newUser)
            db.session.add(newUser)    #Storing
            db.session.commit()
            print("User added to DB")
            return render_template('thankyoupage.html',success=True)
        except Exception as e:
            print(repr(e))
            return render_template("thankyoupage.html",success=False)
        
    else:
        return jsonify({"Response":"Get Request Called"})



#Automated Bday wisher function
@app.route('/sendbdaywish',methods=['GET'])
def sendBdayWish():
    
    # Fetch all users details
    users = models.User.query.all()
    print(users)
    for user in users:
        print("Birthday ",user.dob)
        print("Today's Date",datetime.date.today())
        if(datetime.date.today().day == user.dob.day and datetime.date.today().month == user.dob.month):
            print("here")
            sendEmail(user)
            # sendSMS(user)
    return "success"



#SMS sending route
# @app.route('/sendsms',methods=['POST','GET'])
def sendSMS(user):
    with app.app_context():
        try:
            print("Sending SMS")
            url = "https://www.fast2sms.com/dev/bulkV2"
            number = user.Number
            message = user.message+ "\n -"+user.name
            querystring = {"authorization":"YyvBSlen5O2ALDk4IQUVzsXHCqMRK7i9aNJwp0x3ud1G6fjTbchiQXjoG2RWI8mTJKODE4cA7baFtx9M","message":message,"language":"english","route":"q","numbers":number}
            headers = {
                'cache-control': "no-cache"
            }

            resp = requests.request("GET", url, headers=headers, params=querystring)

            print(resp.text)

            return jsonify({"response":resp.text})
        except Exception as e:
            print(repr(e))
            return jsonify({"response":"Something went wrong"})




#Email sending route
# @app.route('/sendemail',methods=['POST','GET'])
def sendEmail(user):
    with app.app_context():
        try:
            print("Sending Email")    
            msg = Message(
                            'Birthday Wish :)',
                            sender ='birthdaywishingbot@gmail.com',
                            recipients = [user.email]
                        )
            msg.body = user.message+"\n \n -"+user.name
            mail.send(msg)
            print("Email sent")
            return jsonify({"response":"Mail sent"})
        except Exception as e:
                print(repr(e))
                return jsonify({"response":"Something went wrong"})


if __name__ == "__main__":
    print("running")
    scheduler = BackgroundScheduler()
    job = scheduler.add_job( sendBdayWish, 'cron', day_of_week ='mon-sun', hour=23, minute=20,second=15)
    scheduler.start()
    app.run(debug=True)
    # app.run(use_reloader=False)
    
