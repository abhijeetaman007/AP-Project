from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy
# import models
import requests
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime

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


    return render_template("index.html")


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

        # user = request.json  

        newUser = models.User(name=userName,email=userEmail,phone=userPhone,dob=date,message=userMessage)
        # print(newUser)
        try:
            print(db)
            print(newUser)
            db.session.add(newUser)    #Storing
            db.session.commit()
            print("User added to DB")
            return render_template('thankyoupage.html',success=True)


            # return jsonify({"Response":"Success"})
            # return redirect('/')   
        except Exception as e:
            print(repr(e))
            return render_template("thankyoupage.html",success=False)
        
    else:
        return jsonify({"Response":"Get Request Called"})


#SMS sending route
@app.route('/sendsms',methods=['POST','GET'])
def sendSMS():
    with app.app_context():
        try:
            print("Sending SMS")
            url = "https://www.fast2sms.com/dev/bulkV2"
            number = "7091788126"
            message = "Happy Birthday \n - Abhijeet Sinha"
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
@app.route('/sendemail',methods=['POST','GET'])
def sendEmail():
    with app.app_context():
        try:
            print("Sending Email")    
            msg = Message(
                            'Hello testing mailer',
                            sender ='birthdaywishingbot@gmail.com',
                            recipients = ['abhijeetsinha1503@gmail.com']
                        )
            msg.body = 'Final Testing mail'
            mail.send(msg)
            print("Email sent")
            return jsonify({"response":"Mail sent"})
        except Exception as e:
                print(repr(e))
                return jsonify({"response":"Something went wrong"})

# # @app.before_first_request
# def testScheduling():
#     print("Hello from scheduler")
#     print(time.time())
#     time.sleep(100000)

if __name__ == "__main__":
    print("running")
    scheduler = BackgroundScheduler()
    job = scheduler.add_job( sendEmail, 'cron', day_of_week ='mon-sun', hour=18, minute=30,second=10)
    scheduler.start()
    #DB Config
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    # db = SQLAlchemy(app) 

    app.run(debug=True)
    # app.run(use_reloader=False)
    
