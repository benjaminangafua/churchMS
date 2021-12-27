from flask import Flask, Blueprint, render_template, request, jsonify, redirect
from sqlalchemy.sql.expression import join
from churchAPP import db

views = Blueprint('views', __name__)

# print(db)

@views.route("/")
def index():
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    # print(type(memberSum))

    return render_template("index.html", memberSum=memberSum)

@views.route('/calendar')
def calendar():
    return render_template('calendar.html')

@views.route('/charts')
def charts():
    return render_template('charts.html')

@views.route('/dashboard_2')
def dashboard_2():
    return render_template('dashboard_2.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/dashboard')
def dashboard():
    return render_template('index.html')

@views.route('/email')
def email():
    return render_template('email.html')

@views.route('/media_gallery')
def media_gallery():
    return render_template('media_gallery.html')


@views.route('/icons')
def icons():
    return render_template('icons.html')

@views.route('/invoice')
def invoice():
    return render_template('invoice.html')

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/sign-up')
def signUp():
    return render_template('signUp.html')

@views.route('/map')
def map():
    return render_template('map.html')

@views.route('/price')
def price():
    return render_template('price.html')

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/project')
def project():
    return render_template('project.html')

@views.route('/settings')
def setting():
    return render_template('settings.html')

@views.route('/table')
def table():
    return render_template('tables.html')

@views.route('/people')
def people():
    return render_template('people.html')

@views.route('/404_error')
def d404_error():
    return render_template('404_error.html')

    # Members


@views.route('/addMember', methods=["GET", "POST"])
def addNewMember():
    if request.method == "POST":
        member_data = {}
        member_data["relationship"] = request.form.get("relationship")
        member_data["name"]=request.form.get("name")
        member_data["location"] = request.form.get("location")
        member_data["department"] = request.form.get("department")
        member_data["contact"] = request.form.get("contact")
        member_data["role_play"] = request.form.get("role")
        member_data["occupation"] = request.form.get("occupation")
        
        member_data["date_of_birth"] = request.form.get("date_of_birth")
        member_data["gender"] =request.form.get("gender")

        # print( member_data)
        data = db.execute("SELECT * FROM members")
        for name in data:
           if name["name"]==member_data["name"]:
                return "Name already exist"
        
        db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?, date('now'))",
                       member_data["name"], member_data["location"], member_data["department"],  member_data["gender"], member_data["contact"], member_data["relationship"], member_data["occupation"], member_data["role_play"], member_data["date_of_birth"])
        
        return redirect("/")
    return render_template('new-member.html')


@views.route("/member")
def member():
    members = db.execute("SELECT * FROM members ORDER BY id")
    return render_template("member.html",members=members)

@views.route("/new-convert", methods=["GET", "POST"])
def new_convert():
    if request.method == "POST":
        new={}
        new["name"]=request.form.get("name")
        new["location"] = request.form.get("location")
        new["contact"] = request.form.get("contact")


    data = db.execute("SELECT * FROM new_convert")
    if len(data) > 0:
        for name in data:
            if name["name"]== new["name"]:
                return "Nam already taken."

    db.execute("INSERT INTO new_convert(name, contact, location) VALUES(?, ?, ?)")
    return render_template("new-convert.html")




days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]

date = db.execute("SELECT name, strftime('%d',date_of_birth), strftime('%m',date_of_birth) FROM members")


this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])

print(months[this_month])


person_birth_rec = []
birth_day = {}
for datetime in date:
    birth_day["day"] = datetime["strftime('%d',date_of_birth)"]
    birth_day["month"] = datetime["strftime('%m',date_of_birth)"]
    birth_day["name"] = datetime["name"]
    person_birth_rec.append(birth_day)
    

# print(person_birth_rec)

# print("=================>>>>>>>>>>dDD<<<<<<<<<<<<<<<<<++++++++++++++++", month[date])
