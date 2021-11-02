from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app) 

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

        newUser = models.User(id=3,name=user['name'],email=user['email'])
        print(newUser)
        try:
            print(db)
            print(newUser)
            db.session.add(newUser)    #Storing
            db.session.commit()
            print("User added to DB")
            return jsonify({"Response":"Success"})
            # return redirect('/')   
        except:
            return 'There was an issue adding your task'
        
    else:
        return jsonify({"Response":"Get Request Called"})

    # return render_template('index.html',tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)