from flask import Flask, redirect, render_template, request, jsonify, redirect
from cs50 import SQL

app = Flask(__name__)


db = SQL("sqlite:///churchMS.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/newMember", methods=["GET", "POST"])
def newMember():
    if request.method == "GET":
        return render_template("new-member.html")
    else:
        # dp = db.execute("SELECT department FROM members")[0]
        # print(f"=============>>>>>>>>>>>>>{dp}")
        member = {}
        member["name"] = request.form.get("name")
        member["gender"] = request.form.get("gender")
        
        member["position"] = request.form.get("position")
        member["department"] = request.form.get("department")
        member["location"] = request.form.get("location")
        member["contact"] = request.form.get("contact")
        member["marital_status"] = request.form.get("maritalStatus")
        member["occupation"] = request.form.get("occupation")
        member["dob"] = request.form.get("dateOfBirth")
        print(f"==========++>{member['dob']}")
        data = db.execute("SELECT * FROM members")
        for name in data:
           if name["name"]==member["name"]:
                return "Name already exist"
        
        db.execute("INSERT INTO members (name, location, department, gender, contact, marital_status, occupation, role_play,  date_of_birth, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?, date('now'))",
                       member["name"], member["location"], member["department"],  member["gender"], member["contact"], member["marital_status"], member["occupation"], member["position"], member["dob"])
        
        return redirect("/")


def validateNewMemeber(rows):
    for index in range(len(rows)): 
        return rows[index]["name"]

@app.route("/member")
def member():
    members = db.execute("SELECT * FROM members ORDER BY id")
    return render_template("member.html",members=members)
