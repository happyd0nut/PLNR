from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)
app.secret_key = "648fyei838902idjfueu"


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        if session.get('username') != None:
            print(session["username"])
            session.pop("username")
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        user = db_session.query(User).where(User.username==username).first()
        validuser = user != None
        print(validuser)
        #for debugging above
  
        if validuser:
            if user.password == password:
                session["username"] = username
                return redirect(url_for("dashboard"))
            else:
                flash("Your password is incorrect", "info")
                return redirect(url_for("login"))
        else:
            flash("Your username is incorrect", "info")
            return redirect(url_for("login"))
    

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

        userExists = db_session.query(User).where(User.username==username).first() != None
        if userExists:
            flash("That username is taken. Try another.", "info")
            return redirect(url_for("signup"))
        else:
            newUser = User(fname, lname, email, username, password)
            db_session.add(newUser)
            db_session.commit()
            session["username"] = username
            return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/newtask", methods=["POST", "GET"])
def newtask():
    if request.method == 'GET':
       return render_template("newtask.html")
    else:
        task = request.form["task"]
        subject = request.form["subject"]
        duedate = request.form["duedate"]
        notes = request.form["notes"]

        # TODO: add inputs to database

        return redirect(url_for("dashboard"))
        

@app.route("/newsubject", methods=["POST", "GET"])
def newsubject():
    if request.method == 'GET':
       return render_template("newsubject.html")
       
    else:
        subname = request.form["subname"]
        teacher = request.form["teacher"]
        period = request.form["period"]

        subExists = db_session.query(Subject).where(Subject.name==subname).first() != None
        if subExists:
            flash("That subject name already exists. Try another.", "info")
            return redirect(url_for("newsubject"))
        else:
            userid = db_session.query(User).where(User.username == session["username"]).first().id
            newSub = Subject(subname, teacher, period)
            db_session.add(newSub)
            db_session.commit()
            db_session.refresh(newSub)
            db_session.add(Enrollment(userid, newSub.id))
            db_session.commit()
            print(newSub.id)
            return redirect(url_for("dashboard"))
        

        
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
