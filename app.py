from datetime import datetime

import flask
from flask import Flask, render_template, request, url_for, redirect

import pandas as pd


app = Flask(__name__)


authorization = False


# Reading csv file with pandas
df = pd.read_csv("dictionary.csv", delimiter= ",")

def log():
    ip_address = flask.request.remote_addr

    # Splitting user agent data and writing it to a file(logging)
    user_agent = request.headers.get('User-Agent')

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    time_date = "Date and Time: " + now.strftime("%d/%m/%Y %H:%M:%S")

    # Logging
    f = open("loglar/logs.txt", "a")
    f.write("User's IP: " + ip_address + "\n")
    f.write(time_date + "\n")
    f.write("Browser and Operating System Data as User Agent: " + user_agent + "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/loginerror", methods=["GET", "POST"])
def indexLoginError():
    return render_template("indexLoginError.html")

@app.route("/loginsuccessfull", methods=["GET", "POST"])
def indexSuccessfull():
    #log()
    return render_template("indexloginsuccessfull.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Getting input from user by POST method
    if request.method == "POST":
        password = request.form["password"]
        # Checking if input matches with our password
        if password == "mentörşip":
            # Now user can access to logs
            global authorization
            authorization = True
            return redirect(url_for("indexSuccessfull"))
        else:
            return redirect(url_for("indexLoginError"))
    else:
        return render_template("login.html")

@app.route("/EnglishToTurkish", methods=["GET", "POST"])
def english():
    log()
    if request.method == "POST":
        originalInput = request.form["input"]
        word = request.form["input"].lower()
        try:
            # Finding the row number
            rowIndex = df[df['english'].str.lower() == word].index[0]
            # By using the row number, we find the word
            output = "English: " + word.replace("i", "I") + " Turkish: " + df['turkish'][rowIndex]

            f = open("loglar/logs.txt", "a")
            f.write("The searched word and its meaning = " + output + "\n" + "\n")

            return render_template("english.html", data=output)
        except:
            output = "We couldn't find anything for: " + originalInput
            return render_template("english.html", data=output)

    else:
        return render_template("english.html")

@app.route("/TurkishToEnglish", methods=["GET", "POST"])
def turkish():
    log()
    if request.method == "POST":
        originalInput = request.form["input"]
        word = request.form["input"].replace("İ", "I").lower()
        try:
            # Finding the row number
            rowIndex = df[df['turkish'] == word].index[0]
            # By using the row number, we find the word
            output = "Turkish: " + word + " English: " + df['english'][rowIndex]

            f = open("loglar/logs.txt", "a")
            f.write("The searched word and its meaning = " + output + "\n" + "\n" )

            return render_template("turkish.html", data=output)
        except:
            output = "We couldn't find anything for: " + originalInput
            return render_template("turkish.html", data=output)

    else:
        return render_template("turkish.html")

@app.route("/log", methods=["GET", "POST"])
def logspage():
    global authorization
    data = ""
    if authorization == True:
        with open('loglar/logs.txt', 'r') as file:
            data = file.read().split('\n')
        return render_template("log.html", data=data)
    else:
        return redirect(url_for("indexLoginError"))

if __name__ == "__main__":
    app.run(debug=True)
