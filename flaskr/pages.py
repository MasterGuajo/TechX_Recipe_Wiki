from flask import render_template, request, flash, redirect, jsonify
from flaskr.backend import Backend
import hashlib

# Stuff imported for file upload
# from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename


import base64
import io


# Extension that the user is allowed to upload
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf'}

# from flaskr.backend import Backend

from flaskr.user import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
"""
run cmds:

cd project
chmod a+x run-flask.sh
./run-flask.sh
"""

def make_endpoints(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_message = u"Please log in first."

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    # Flask uses the "app.route" decorator tos call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def home():
        if current_user.is_authenticated:
            return render_template("main.html", name = current_user.username)
        return render_template("main.html")

    @app.route("/pages")
    def pages():
        if current_user.is_authenticated:
            return render_template("pages.html", pages=Backend.get_all_pages(None), name = current_user.username)
        else:
            return render_template("pages.html", pages=Backend.get_all_pages(None))


    @app.route("/pages/<int:page_id>")
    def show_page(page_id):
        if current_user.is_authenticated:
            return render_template("page.html", page_data=Backend.get_wiki_page(None, page_id), name = current_user.username)
        else:
            return render_template("page.html", page_data=Backend.get_wiki_page(None, page_id))

    @app.route("/about", methods=['GET'])
    def about():
        
        # image = Backend.get_image(None,'plswork.jpg')

        # return render_template("about.html", show = image.decode('utf-8'))

        author_images = ['plswork.jpg','cat.jpg','hamster.png']

        for index,file_name in enumerate(author_images):
            image = Backend.get_image(None,file_name)
            author_images[index] = image.decode('utf-8')

        return render_template("about.html", show = author_images)
    
    # Checks that the file being uploaded is allowed
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

    # Here the users upload their files
    @app.route("/upload", methods=['GET', 'POST'])
    @login_required
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
               
                return render_template("upload.html",message = message, name = current_user.username)

        return render_template("upload.html", name = current_user.username)

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/check_signup", methods=['POST'])
    def check_signup():
        user_name = request.form["Username"]
        password = "prefix" + request.form["Password"] 
        hash = hashlib.blake2b(password.encode()).hexdigest()
        user = {user_name : str(hash)}
        flask_user = User(user_name)
        if Backend.sign_up(None,user, user_name):
            login_user(flask_user)
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
        flask_user = User(user_name)
        if Backend.sign_in(None,user, user_name):
            login_user(flask_user)
            return redirect('/home')
        else: 
            return "error"

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect('/home')


    # TODO(Project 1): Implement additional routes according to the project requirements.
        
