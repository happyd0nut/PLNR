from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "648fyei838902idjfueu"

# TODO: Fill in methods and routes

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        # TODO: check database for correct user

        return redirect(url_for("dashboard"))
    
         

        

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # TODO: check database for correct input

        return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/newtask", methods=["POST", "GET"])
def newtask():
    if request.method == 'GET':
       return render_template("newtask.html")

        
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
