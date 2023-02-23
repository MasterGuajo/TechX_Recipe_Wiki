from flask import render_template

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
        return render_template("pages.html", pages=Backend.get_all_pages(0))

    @app.route("/pages/<int:page_id>")
    def show_page(page_id):
        return render_template("page.html", page_data=Backend.get_wiki_page(0,page_id))

    @app.route("/about")
    def about():
        return render_template("about.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
