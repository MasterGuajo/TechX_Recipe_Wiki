from flask import render_template, request, flash, redirect, jsonify
from flaskr.backend import Backend
import hashlib

# Stuff imported for file upload
# from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# Extension that the user is allowed to upload
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}

from flaskr.backend import Backend

"""
run cmds:

cd project
chmod a+x run-flask.sh
./run-flask.sh
"""

def make_endpoints(app):

    # Flask uses the "app.route" decorator tos call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    @app.route("/home")
    @app.route("/index")
    def home():
        return render_template("main.html")

    @app.route("/pages")
    def pages():
        return render_template("pages.html", pages=Backend.get_all_pages(None))

    @app.route("/pages/<int:page_id>")
    def show_page(page_id):
        return render_template("page.html", page_data=Backend.get_wiki_page(None, page_id))

    @app.route("/about")
    def about():
        return render_template("about.html", author_images=None)
    
    # Checks that the file being uploaded is allowed
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

    # Here the users upload their files
    @app.route("/upload", methods=['GET', 'POST'])
    def upload():

        if request.method == 'POST':

            # Check that it's a valid file
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            # If valid, we pass it to the backend in order to upload to our bucket
            if file and allowed_file(file.filename):
                    
                filename = secure_filename(file.filename)
                file.save(os.path.join(filename))

                Backend.upload(None,'nrjcontent',file.filename)
                message = "Succesfully uploaded"
               
                return render_template("upload.html",message = message)

        return render_template("upload.html")

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
        
