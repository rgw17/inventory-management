from logging import error
from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sys
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import csv
import hashlib
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
app.secret_key = "random dancing"
con = sqlite3.connect('item.db')

# Instantiate the database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    salt = db.Column(db.String(200), unique=False)
    key = db.Column(db.String(200), unique=False)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False) # db.ForeignKey('category.category'), 
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200), nullable=False)
    added_by = db.Column(db.String(30), nullable=False)
    serialNo = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    receipt = db.Column(db.Boolean, default=False, nullable=False)
    # Function to return string when we add something
    def __rep__(self):
        return '<Unique ID %r>' % self.id



# class Category(db.Model):
#     __tablename__ = 'category'
#     category = db.Column(db.String(100), primary_key=True, nullable=False)

@app.route("/")
def index():
    errorMessage = ""
    if 'errorMessage' in session:
        errorMessage = session['errorMessage']
    session['errorMessage'] = ""

    return render_template("index.html", errorMessage=errorMessage)

@app.route("/writecsv")
def unknown():
    items = Item.query.order_by(Item.date_created)
    masterList = []
    header = ['ID','Brand','Category','Owner','Date added','Serial no.','Added by','Location','Receipt']
    for item in items:
        stuff=[]
        stuff.append(item.id)
        stuff.append(item.description)
        stuff.append(item.category)
        stuff.append(item.owner)
        stuff.append(item.date_created)
        stuff.append(item.serialNo)
        stuff.append(item.added_by)
        stuff.append(item.location)
        if item.receipt:
            stuff.append("Yes")
        else:
            stuff.append("No")
        masterList.append(stuff)
    with open('inventory.csv', mode='w', newline="") as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(header)
        for sublist in masterList:
            employee_writer.writerow(sublist)
    return send_file("inventory.csv", as_attachment=True)

@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.form.get("username")

    try:
        user = User.query.filter_by(username=username).first()
        new_key = hashlib.pbkdf2_hmac('sha256', request.form.get("password").encode('utf-8'), user.salt, 100000)

        if user.key == new_key:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            session['errorMessage'] = "Invalid credentials."
            return redirect(url_for('index'))
        
    except Exception as e:
        session['errorMessage'] = "Invalid credentials."
        return redirect(url_for('index'))

@app.route("/dashboard", methods=['POST','GET'])
@login_required
def dashboard():
    items = Item.query.order_by(Item.date_created)
    return render_template("dashboard.html", username=current_user.username, items=items)
    

@app.route('/home')
@login_required
def home():

    # if 'username' in session:
    #     username = session['username']
    # else:
    #     username = request.form.get("username")
    #     session['username'] = username
    items = Item.query.order_by(Item.date_created)

    return render_template("dashboard.html", username=current_user.username, items=items)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['errorMessage'] = "You are logged out!"
    return redirect(url_for('index'))

@app.route("/view_inventory")
@login_required
def view_inventory():
    return render_template("inventory.html")

@app.route("/add_item", methods=['POST','GET'])
def create_item():
    if request.method == 'GET':
        return render_template("createItem.html")
    if request.method == 'POST':
        # add item to database
        errorMessage = ""
        description = None
        serialNo = "N/A"
        owner = "N/A"
        try:
            description = request.form["description"]
            category = request.form['category']
            location = request.form['location']
            receipt = request.form.getlist('receipt')
            if receipt:
                receipt = True
            else:
                receipt = False
        except Exception as e:
            errorMessage="Error: you left one or more fields empty."
            return render_template("error.html", errorMessage=errorMessage)
            
        if not description:
            errorMessage="Error: you left one or more fields empty."
            return render_template("error.html", errorMessage=errorMessage)
        if category == "Laptop" or category == "Monitor":
            try:
                owner = request.form['radioBox']
                serialNo = request.form['serialNo']
            except:
                errorMessage="There was an error processing your request."
                return render_template("error.html", errorMessage=errorMessage)
        if category == "Headset":
            try:
                owner = request.form['radioBox']
            except:
                errorMessage="There was an error processing your request."
                return render_template("error.html", errorMessage=errorMessage)
        new_item = Item(description=description, category=category, added_by=current_user.username, serialNo=serialNo, owner=owner, location=location, receipt=receipt)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            print(e, file=sys.stderr)
            errorMessage = 'There was an error adding your item.'
            return render_template("error.html", errorMessage=errorMessage)

@app.route("/remove_item<int:id>", methods=['POST','GET'])
@login_required
def remove_item(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('dashboard'))
    except Exception as e:
        errorMessage = 'There was an error removing your item.'
        return render_template("error.html", errorMessage=errorMessage)


@app.route("/remove_item_page", methods=['POST','GET'])
@login_required

def remove_item_page():
    if request.method == 'GET':
        return render_template("removeItem.html")
    if request.method == 'POST':
        id = request.form['id']
        print("1 ------------------- ", file=sys.stderr)
        try:
            item_to_delete = Item.query.get_or_404(id)
            db.session.delete(item_to_delete)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(e, file=sys.stderr)
            print("ERROR ------------------- ", file=sys.stderr)
            errorMessage = 'There was an error removing your item.'
            return render_template("error.html", errorMessage=errorMessage)

@app.route("/create_category", methods=['POST','GET'])
def create_category():
    if request.method == 'GET':
        print("TEST ---------------------------", file=sys.stderr)
        return render_template("createCategory.html")
    if request.method == 'POST':
        # add item to database
        return redirect(url_for('dashboard'))

@app.route("/remove_category", methods=['POST','GET'])
def remove_category():
    if request.method == 'GET':
        print("TEST ---------------------------", file=sys.stderr)
        return render_template("removeCategory.html")
    if request.method == 'POST':
        # add item to database
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
