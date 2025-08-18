from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)





@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template('signup and login/signup.html')

@app.route("/login", methods=["GET"])
def login_page():
    return render_template('signup and login/login.html')
@app.route("/Add_Player")
def Create_Player():
    return render_template('../Add/Add_Player.html')

@app.route("/Cantina")
def Cantina():
    return render_template('../Add/Cantina.html')
@app.route("/Add_Equipo")
def hell():
    return render_template('../Add/Add_Equipo.html')

@app.route("/Add_Match")
def Create_Match():
    return render_template('../Add/Add_Match.html')

@app.route("/Add_Staff")
def Create_Staff():
    return render_template('../Add/Add_Staff.html')



if __name__ == "__main__":
    app.run(debug=True)