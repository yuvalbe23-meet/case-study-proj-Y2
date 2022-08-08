
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyBItsyl9KLYXJ9R0cFNRO2rT2C-qTYQle4",
  "authDomain": "topwatch-bfbb8.firebaseapp.com",   
  "projectId": "topwatch-bfbb8",
  "storageBucket": "topwatch-bfbb8.appspot.com",
  "messagingSenderId": "133205884441",
  "appId": "1:133205884441:web:40ca8c4370c99a94fef488",
  "measurementId": "G-BZ2K12N6XS",
  "databaseURL":"https://topwatch-bfbb8-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db= firebase.database()

if db.child("WaitingList").get().val() is None:
    db.child("WaitingList").set(0)

#HOME
@app.route('/', methods=['GET','POST'])
def home():
    return render_template("index.html") 

#ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

#DEMO 
@app.route('/demo')
def demo():
    return render_template('demo.html')

#FEATURES
@app.route('/features')
def features():
    return render_template('features.html')









@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    eror=""
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']

        try: 
            login_session['user']= auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('land'))
            
        except:
            eror="Not Working"
            
    return render_template("signin.html")

   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    eror=""
    print("4567")

    if request.method == 'POST':
        print("we get here")
        email= request.form['email']
        password= request.form['password']

        user={"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"waitingnum": 0}
        try: 
            login_session['user']= auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            print("12345")
            return redirect(url_for('signin'))
        except:
            eror="Not Working"
    return render_template("signup.html",)



@app.route('/land', methods=['GET', 'POST'])
def land():
    return render_template("land.html", users= db.child("Users").child(login_session['user']['localId']).get().val()['full_name'])




@app.route('/product', methods=['GET' , 'POST'])
def product():
    return render_template("product.html")

@app.route('/wating', methods=['GET','POST'])
def wating():
    if request.method=='POST':
        if db.child("WaitingList").get().val() != None:
            s=int(db.child("WaitingList").get().val())+1
            db.child("WaitingList").set(s)
            w=db.child("Users").child(login_session['user']['localId']).get().val()
            w['waitingnum']=s
            db.child("Users").child(login_session['user']['localId']).update(w)
    return render_template("wating.html", userr= db.child("Users").child(login_session['user']['localId']).get().val()['waitingnum'])

@app.route('/last', methods=['GET','POST'])
def last():
    return render_template("last.html")

if __name__ == '__main__':
    app.run(debug=True)