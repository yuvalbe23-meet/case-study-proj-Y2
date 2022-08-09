
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyCbS4QZYb5Zs6GPw153KjqMN3OQmUGhdd4",
  "authDomain": "careunity-bdecb.firebaseapp.com",
  "projectId": "careunity-bdecb",
  "storageBucket": "careunity-bdecb.appspot.com",
  "messagingSenderId": "252598637014",
  "appId": "1:252598637014:web:607095a064d325af559477",
  "measurementId": "G-9VJCG31XFR",
  "databaseURL":"https://careunity-bdecb-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db= firebase.database()



#HOME
@app.route('/', methods=['GET','POST'])
def home():
    eror=""
    print("4567")

    if request.method == 'POST':
        print("we get here")
        email= request.form['email']

        user={"name": request.form['name'],"email": request.form['email'],"phone": request.form['phone']}
        db.child("Users").push(user)
        try: 
            
            return redirect(url_for('demo'))
        except:
            eror="Not Working"
    return render_template("index.html",)

#ABOUT
@app.route('/about' ,methods=['GET','POST'])
def about():
    return render_template('about.html')

#DEMO 
@app.route('/demo', methods=['GET','POST'])
def demo():
    return render_template('demo.html')

#FEATURES
@app.route('/features', methods=['GET','POST'])
def features():
    return render_template('features.html')













   









if __name__ == '__main__':
    app.run(debug=True)