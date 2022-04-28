from flask import Flask, request, flash, redirect, url_for
import os
import ast
from flask import render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)

#defining list of email
emailList = []

#creating emails.txt file
open('emails.txt','a')
newfile = open('emails.txt').read()

#for every new session, checks if the file has email, if it does then it adds the emails from file to the email list we created above.
if os.stat('emails.txt').st_size != 0:
    emailList1 = ast.literal_eval(newfile)
    print(emailList1)
    print(type(emailList1))
    emailList.extend(emailList1)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/schedule.html')
def schedule():
    return render_template("schedule.html")

@app.route('/', methods=['POST'])
def my_form_post():
    inputEmail = request.form['email']

    #checks if email already exist in the list
    for e in emailList:
        if e == inputEmail:
            flash('Error! Email already in the list!!') #flashes message in index.html
            return redirect(url_for('index'))

    #adding newly registered email
    emailList.append(inputEmail)
    if request.method == 'POST':
            with open('emails.txt', 'w') as f:
                f.write(str(emailList))
            flash('Email successfully signed up!!')
    return render_template('index.html')
