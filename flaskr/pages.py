from flask import render_template, request, flash, redirect
from flaskr.backend import Backend
import hashlib
def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/check_signup", methods=['POST'])
    def check_signup():
        user_name = request.form["Username"]
        password = "prefix" + request.form["Password"] 
        hash = hashlib.blake2b(password.encode()).hexdigest()
        user = {user_name : str(hash)}
        if Backend.sign_up(None,user, user_name):
            return redirect('/')
        else:
            return "error"
        

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/check_login", methods=['POST'])
    def check_login():
        user_name = request.form["Username"]
        password = "prefix" + request.form["Password"] 
        hash = hashlib.blake2b(password.encode()).hexdigest()
        user = {"User" : user_name, "Pass" : str(hash)}
        if Backend.sign_in(None,user, user_name):
            return redirect('/')
        else: 
            return "error"


    # TODO(Project 1): Implement additional routes according to the project requirements.
