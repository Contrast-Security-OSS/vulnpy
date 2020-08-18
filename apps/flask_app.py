from flask import Flask, redirect

from vulnpy.flask.blueprint import vulnerable_blueprint

app = Flask(__name__)
app.register_blueprint(vulnerable_blueprint)


@app.route("/")
def index():
    return redirect("/vulnpy/")
