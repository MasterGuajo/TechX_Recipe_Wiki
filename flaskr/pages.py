from flask import render_template, request, flash, redirect, jsonify
from flaskr.backend import Backend
import hashlib
from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from flaskr.user import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import base64
import io

# Extension that the user is allowed to upload
#ALLOWED_EXTENSIONS = {'png','jpg','jpeg','pdf','json'}
ALLOWED_EXTENSIONS = {'json'}
"""Route Manager for Program

Uses route decorators to designate app's routes. Returns jinja html templates
to load pages.
"""


def make_endpoints(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def home():
        if current_user.is_authenticated:
            return render_template("main.html", name=current_user.username)
        return render_template("main.html")

    """Endpoint for homepage.

    Loads home page with jinja template.

    Returns:
        A jinja render_template call with the corresponding template - main.html. Changes
        param if user is logged in.
    """

    @app.route("/pages")
    def pages():
        if current_user.is_authenticated:
            return render_template("pages.html",
                                   pages=Backend.get_all_pages(None),
                                   name=current_user.username)
        else:
            return render_template("pages.html",
                                   pages=Backend.get_all_pages(None))

    """Endpoint for wiki pages.

    Loads wiki page overview with jinja template. Calls Backend function to retrieve the
    corresponding data.

    Returns:
        A jinja render_template call with the corresponding template - pages.html. Loads
        data with Backend function call. Changes param if user is logged in.
    """

    @app.route("/pages/<int:page_id>")
    def show_page(page_id):
        if current_user.is_authenticated:
            return render_template("page.html",
                                   page_data=Backend.get_wiki_page(
                                       None, page_id),
                                   name=current_user.username)
        else:
            return render_template("page.html",
                                   page_data=Backend.get_wiki_page(
                                       None, page_id))

    """Endpoint for specific wiki page.

    Parametrized endpoint for specific wiki page, loads page matching an ID with the jinja 
    template (page.html). Calls Backend function for loading the matching data.

    Returns:
        A jinja render_template call with the corresponding template - page.html. Loads
        data with Backend function call. Changes param if user is logged in.
    """

    @app.route("/about", methods=['GET'])
    def about():

        author_images = ['plswork.jpg', 'cat.jpg', 'hamster.png']

        for index, file_name in enumerate(author_images):
            image = Backend.get_image(None, file_name)
            author_images[index] = image.decode('utf-8')

        return render_template("about.html", show=author_images)

    """Endpoint for about page.

    Loads wiki page with corresponding jinja template - about.html. Calls backend
    function storing corresponding author images to list, which is passed to return.

    Returns:
        A jinja render_template call with the corresponding template - about.html. Grabs
        data from list populated by Backend.get_image() call.
    """

    # Checks that the file being uploaded is allowed
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

    """ Checks that a given file has an allowed format

    Checks if the termination of a file is in the specified list of allowed formats

    Args:
        Takes in a file

    Returns:
        Returns true or false depending on if its valid or not
    """
    # Here the users upload their files
    @app.route("/upload", methods=['GET', 'POST'])
    @login_required
    def upload():

        if request.method == 'POST':

            # Check that it's a valid file
            if 'file' not in request.files:
                # flash('No file part')
                message = "No file part"
                return render_template("upload.html",
                                       message=message,
                                       name=current_user.username)
                # return redirect(request.url)

            file = request.files['file']

            if file.filename == '':

                message = "No selected file"
                return render_template("upload.html",
                                       message=message,
                                       name=current_user.username)

                # flash('No selected file')
                # return redirect(request.url)

            if not (allowed_file(file.filename)):
                message = "Not a valid file format"
                return render_template("upload.html",
                                       message=message,
                                       name=current_user.username)

            # If valid, we pass it to the backend in order to upload to our bucket
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(filename))

                Backend.upload(None, 'nrjcontent', file.filename)
                message = "Succesfully uploaded"

                return render_template("upload.html",
                                       message=message,
                                       name=current_user.username)

        return render_template("upload.html", name=current_user.username)

    """ Uploads file to specified path in bucket

    Using a POST method, we obtain from the user a file that will be uploaded in the bucket. Before uploading,
    we check that its a valid file and that they selected one. If it passes the test, we can upload it. The user is required to 
    be logged in in order to access this

    Args:
        Using POST we obtain a file
    
    Uses:
        allowed_file in order to check that the file is valid

    Returns:
        A render template of the HTML along with a custom message displaying whether or not the file was uploaded succesfully
    """

    @app.route("/signup")
    def signup():
        """
        Renders sign up form template.
        """
        return render_template("signup.html")

    @app.route("/check_signup", methods=['POST'])
    def check_signup():
        """Acquire form data, encrypt password,
        create User object, and call backend to
        authenticate said User. If backend successfully
        authenticates user, redirect back to home. 
        Otherwise return error message.   

        Args:
          user_name: String that holds username.
          password: String that holds password with prefix to be hashed.
        """
        backend = Backend(storage.Client())
        user_name = request.form["Username"]
        password = "prefix" + request.form["Password"]
        hash = hashlib.blake2b(password.encode()).hexdigest()
        flask_user = User(user_name)
        if backend.sign_up(flask_user, str(hash)):
            login_user(flask_user)
            return redirect('/home')
        else:
            return "Sign Up Failed."

    @app.route("/login")
    def login():
        """
        Renders login form template.
        """
        return render_template("login.html")

    @app.route("/check_login", methods=['POST'])
    def check_login():
        """Acquire form data, encrypt password,
        create User object, and call backend to
        authenticate said User. If backend successfully
        authenticates user, redirect back to home. 
        Otherwise return error message.   

        Args:
          user_name: String that holds username.
          password: String that holds password with prefix to be hashed.
        """
        user_name = request.form["Username"]
        password = "prefix" + request.form["Password"]
        hash = hashlib.blake2b(password.encode()).hexdigest()
        flask_user = User(user_name)
        if Backend.sign_in(None, flask_user, str(hash)):
            login_user(flask_user)
            return redirect('/home')
        else:
            return "Login Failed"

    @app.route("/logout")
    @login_required
    def logout():
        """
        Renders login form template.
        """
        logout_user()
        return redirect('/home')

    @app.route("/profile_page", methods=['POST','GET'])
    @login_required
    def profile_page():
        # Gets all recipe categories available for display
        recipe_categories = Backend.get_recipe_categories(None)

        if request.method == "POST":

            if "reset" in request.form:
                Backend.reset_preferences(None,current_user)
            else:
                # Store preferences
                Backend.store_preferences(None,current_user,request.form.getlist('category_chosen'))

         # Gets current user preferences
        user_preferences = Backend.get_preferences(None,current_user)

        # Filter recipes
        recipes = Backend.get_selected_categories(None,user_preferences)

        return render_template("profile_page.html", recipe_categories = recipe_categories, recipes = recipes, name = current_user.username)
