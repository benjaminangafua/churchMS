from re import S
from flask import Flask, Blueprint, render_template, request, jsonify, redirect
from sqlalchemy.sql.expression import join
from churchAPP import db

views = Blueprint('views', __name__)

@views.route("/")
def index():

    # Birthday's section
    data = db.execute("SELECT * FROM birthday")
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    
    # Department's Section
    deparmentSum = db.execute('SELECT COUNT(DISTINCT(department)) FROM members')[0]['COUNT(DISTINCT(department))']

    if len(data) > 0:
    
        this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
        this_day = int(db.execute("SELECT strftime('%d','now');")[0]["strftime('%d','now')"])
        birth_record = db.execute(f"SELECT COUNT(*) FROM birthday WHERE month = {this_month}")[0]['COUNT(*)']
        today_birtday = db.execute(f"SELECT COUNT(DISTINCT(name)) FROM birthday WHERE day = {this_day}")[0]['COUNT(DISTINCT(name))']
        
        print(birth_record)
        # Member's Section
        return render_template("index.html", numOfBirthday=birth_record, todayNumOfBirthday=today_birtday, deparmentSum=deparmentSum, memberSum=memberSum)
    
    return render_template("index.html", deparmentSum=deparmentSum, memberSum=memberSum)

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
@views.route('/general-element')
def general():
    return render_template('general_elements.html')

@views.route('/add-new-member', methods=["GET", "POST"])
def addNewMember():
    data = db.execute("SELECT * FROM members")
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
        if len(data) > 0:
            for name in data:
                if name["name"]==member_data["name"]:
                    message =  "Name already exist"
                    apology(message)
        db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?, date('now'))",
                       member_data["name"], member_data["location"], member_data["department"],  member_data["gender"], member_data["contact"], member_data["relationship"], member_data["occupation"], member_data["role_play"], member_data["date_of_birth"])
        
        dob = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
       
        DATEOFBIRTH = db.execute("SELECT * FROM birthday")
        
        for new in dob:

            # Check for duplicate
            if len(data) > 0:
                print("enter 2nd condition----------------->>>>>>>>")
                if len(DATEOFBIRTH) > 0:
                    print("outside loop----------------->>>>>>>>")
                    for name in DATEOFBIRTH:
                        print("enter loop----------------->>>>>>>>")
                        if name["name"]== new["name"]:

                            message = "Nam already taken."
                            apology(message)
                        # Insert Date of birth
                        db.execute("INSERT INTO birthday(name, day, month) VALUES(?, ?, ?)", new["name"], new["Day"], new["Month"])
            db.execute("INSERT INTO birthday(name, day, month) VALUES(?, ?, ?)", new["name"], new["Day"], new["Month"])
            
        return redirect("/")
    return render_template('add-new-member.html')


@views.route("/member")
def member():
    members = db.execute("SELECT * FROM members ORDER BY id")
    return render_template("member.html",members=members)

@views.route("/add-new-convert", methods=["GET", "POST"])
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
                    message = "Nam already taken."
                    apology(message)

            db.execute("INSERT INTO new_convert(name, contact, location) VALUES(?, ?, ?, date('now'))", new["name"], new["contact"], new["location"])
            return redirect("/convert")

        else:
            db.execute("INSERT INTO new_convert(name, contact, location) VALUES(?, ?, ?, date('now'))", new["name"], new["contact"], new["location"])
            return redirect("/convert")

    return render_template("add-new-convert.html")

@views.route("/convert")
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

@views.route("/add-first-timer", methods=["GET", "POST"])
def first_timer():
    if request.method == "POST":
        new={}
        new["name"]=request.form.get("name")
        new["location"] = request.form.get("location")
        new["contact"] = request.form.get("contact")
        new["gender"] = request.form.get("gender")
        data = db.execute("SELECT * FROM first_time_visitors")
        if len(data) > 0:
            for name in data:
                if name["name"]== new["name"]:
                    message = "Nam already taken."
                    apology(message)

            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))", new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/vissitor")

        else:
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender) VALUES(?, ?, ?, ?, date('now'))", new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/visitor")

    return render_template("add-first-timers.html")

@views.route("/visitor")
def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)
    

@views.route("/birthday")
def birthday():
    
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT * FROM birthday")
        
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)
    
def apology(message):
    return render_template("apology.html", message=message)