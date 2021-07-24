from flask import Flask, render_template, request, redirect, url_for, session
import sys
app = Flask(__name__)
app.secret_key = "random dancing"

@app.route("/")
def hello_world():
    session.pop('username')
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def console():
    
    if 'username' in session:
        username = session['username']
        print("TEST ---------------------------", file=sys.stderr)
    else:
        username = request.form.get("username")
        session['username'] = username
        print("username in ---------------------------", file=sys.stderr)

    return render_template("console.html", username=username)

@app.route("/view_inventory")
def view_inventory():
    return render_template("inventory.html")

@app.route("/add_item", methods=['POST','GET'])
def create_item():
    if request.method == 'GET':
        username = ""
        return render_template("createItem.html")
    if request.method == 'POST':
        # add item to database
        if 'username' in session:
            username = session['username']
        return redirect(url_for('console'))

@app.route("/remove_item", methods=['POST','GET'])
def remove_item():
    if request.method == 'GET':
        print("TEST ---------------------------", file=sys.stderr)
        return render_template("removeItem.html")
    if request.method == 'POST':
        # add item to database
        return redirect(url_for('console'))

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


