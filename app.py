from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import models
import requests
from flask_mail import Mail, Message
import smtplib

app = Flask(__name__)

#DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app) 


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
    # return "Hello"
    return render_template("index.html")


# Testing DB connection route
@app.route('/test',methods=['POST','GET']) 
def test():
    if request.method == 'POST':    
        user = request.json  
        print("User obj ",user)

        newUser = models.User(id=4,name=user['name'],email=user['email'])
        print(newUser)
        try:
            print(db)
            print(newUser)
            db.session.add(newUser)    #Storing
            db.session.commit()
            print("User added to DB")
            return jsonify({"Response":"Success"})
            # return redirect('/')   
        except Exception as e:
            print(repr(e))
            return 'There was an issue adding your task'
        
    else:
        return jsonify({"Response":"Get Request Called"})

    # return render_template('index.html',tasks=tasks)




#SMS sending route
@app.route('/sendsms',methods=['POST','GET'])
def sendSMS():
    try:
        print("Sending SMS")
        url = "https://www.fast2sms.com/dev/bulkV2"
        number = "7091788126"
        message = "Happy Birthday"
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
    try:
        print("Sending Email")    
        msg = Message(
                        'Hello testing mailer',
                        sender ='birthdaywishingbot@gmail.com',
                        recipients = ['abhijeetsinha1503@gmail.com']
                    )
        msg.body = 'Hello Flask message sent from Flask-Mail'
        mail.send(msg)
        
        return jsonify({"response":"Mail sent"})
    except Exception as e:
        print(repr(e))
        return jsonify({"response":"Something went wrong"})

if __name__ == "__main__":
    app.run(debug=True)