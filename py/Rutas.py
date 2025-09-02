from flask import Flask, render_template,Blueprint, request, jsonify, redirect, url_for
from flask_cors import CORS
from jinja2 import TemplateNotFound
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from py.apis import CursoUsuario  

rutas = Blueprint('rutas', __name__,template_folder='templates')



@rutas.route("/signup", methods=["GET"])
def signup_page():
    return render_template('signup and login/signup.html')

@rutas.route("/login", methods=["GET"])
def login_page():
    return render_template('signup and login/login.html')

@rutas.route("/curso/<string:codigo>")
def curso(codigo):
    conexiones = CursoUsuario.query.filter_by(codigo=codigo,email=current_user.email).all()
    if not conexiones:
        return render_template('error.html')
    return render_template('curso.html', codigo=codigo)




