from flask import Flask, render_template,Blueprint, request, jsonify, redirect, url_for
from flask_cors import CORS
from jinja2 import TemplateNotFound

rutas = Blueprint('rutas', __name__,template_folder='templates')



@rutas.route("/signup", methods=["GET"])
def signup_page():
    return render_template('signup and login/signup.html')

@rutas.route("/login", methods=["GET"])
def login_page():
    return render_template('signup and login/login.html')

@rutas.route("/curso/<int:id>")
def curso(id):
    return render_template('curso.html', id=id)




if __name__ == "__main__":
    rutas.run(debug=True)