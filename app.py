from flask import Flask, render_template, request, redirect, url_for, session
import sys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
db = SQLAlchemy(app)
app.secret_key = "random dancing"

# Create database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False) # db.ForeignKey('category.category'), 
    quantity = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200), nullable=False)
    
    # Function to return string when we add something
    def __rep__(self):
        return '<Unique ID %r>' % self.id



# class Category(db.Model):
#     __tablename__ = 'category'
#     category = db.Column(db.String(100), primary_key=True, nullable=False)




@app.route("/")
def hello_world():
    session.pop('username')
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def console():
    
    if 'username' in session:
        username = session['username']
    else:
        username = request.form.get("username")
        session['username'] = username
    items = Item.query.order_by(Item.date_created)

    return render_template("console.html", username=username, items=items)

@app.route("/view_inventory")
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
        try:
            description = request.form["description"]
            category = request.form['category']
        except:
            errorMessage="Error: you left one or more fields empty."
            return render_template("error.html", errorMessage=errorMessage)
        if not description:
            errorMessage="Error: you left one or more fields empty."
            return render_template("error.html", errorMessage=errorMessage)
        new_item = Item(description=description, category=category)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('console'))

        except Exception as e:
            print(e, file=sys.stderr)
            errorMessage = 'There was an error adding your item.'
            return render_template("error.html", errorMessage=errorMessage)

@app.route("/remove_item<int:id>", methods=['POST','GET'])
def remove_item(id):
    item_to_delete = Item.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('console'))
    except Exception as e:
        errorMessage = 'There was an error removing your item.'
        return render_template("error.html", errorMessage=errorMessage)


@app.route("/remove_item_page", methods=['POST','GET'])
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
            return redirect(url_for('console'))
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
        return redirect(url_for('console'))

@app.route("/remove_category", methods=['POST','GET'])
def remove_category():
    if request.method == 'GET':
        print("TEST ---------------------------", file=sys.stderr)
        return render_template("removeCategory.html")
    if request.method == 'POST':
        # add item to database
        return redirect(url_for('console'))


