from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)
app.secret_key = "648fyei838902idjfueu=="


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        if session.get('username') != None:
            session.pop("username")
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        validuser = db_session.query(User).where(User.username==username).first() != None
        #for debugging above
  
        if validuser:
            user = db_session.query(User).where(User.username == username).first()
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

            # newSub = Subject(name="Welcome!")
            # db_session.add(newSub)
            # db_session.commit()
            # db_session.refresh(newSub)
            
            # user_id = db_session.query(User).where(User.username == session["username"]).first().id
            # db_session.add(Enrollment(user_id, newSub.id))
            # db_session.add(Task(name="Create a new Subject!", subject_id=newSub.id, user_id=user_id))
            # db_session.commit()

            return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    name = db_session.query(User).where(User.username==session["username"]).first().first_name
    deck = db_session.query(User).where(User.username == session["username"]).first().subjects
    print(deck)
    return render_template("dashboard.html", deck=deck,name=name)


@app.route("/newtask", methods=["POST", "GET"])
def newtask():
    if request.method == 'GET':
       return render_template("newtask.html")
    else:
        task = request.form["task"]
        subject = request.form.get("subject")
        duedate = request.form["duedate"]
        notes = request.form["notes"]

        user_id = db_session.query(User).where(User.username == session["username"]).first().id
        subjectList = db_session.query(User).where(User.username == session["username"]).first().subjects
        for i in subjectList: # looks for subject in database
            if i.name == subject:
                db_session.add(Task(name=task, subject_id=i.id, user_id=user_id, due_date=duedate, notes=notes))
                db_session.commit()
                return redirect(url_for("dashboard"))
        flash("That subject does not exist. Try another.", "info")
        return render_template("newtask.html", subjectList = subjectList)

        

@app.route("/newsubject", methods=["POST", "GET"])
def newsubject():
    if request.method == 'GET':
       return render_template("newsubject.html")
       
    else:
        subname = request.form["subname"]
        teacher = request.form["teacher"]
        period = request.form["period"]

        userid = db_session.query(User).where(User.username == session["username"]).first().id
        subExists = db_session.query(Subject).where((Subject.name==subname) & (Subject.user_id == userid)).first() != None
        if  subExists:
            flash("That subject name already exists. Try another.", "info")
            return redirect(url_for("newsubject"))
        else:
            userid = db_session.query(User).where(User.username == session["username"]).first().id
            newSub = Subject(name=subname, user_id=userid, teacher=teacher, period=period)
            db_session.add(newSub)
            db_session.commit()
            return redirect(url_for("dashboard"))
        
# TODO:
# - add back logout button
# - ability to sort by date
# - ability to cross out!!
        
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
