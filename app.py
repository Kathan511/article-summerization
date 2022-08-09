from flask import Flask,render_template,request
import main3
import smtplib
from sys import *
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://TG:Kathan511@cluster0.814yu.mongodb.net/WebData?retryWrites=true&w=majority")
db = client['WebData']
posts = db.articles


app=Flask(__name__)
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/submit",methods=["POST"])
def submit():
    if request.method=="POST":
        wekiText=request.form["wekiText"]
        articleText=request.form['articleText']
        sentNumber=int(request.form['sentNumber'])
        if len(wekiText)!=0:
            summerized_text=main3.weki_summary(wekiText,sentNumber)

            posts.insert_one({"article":summerized_text})
            f=open("summ.txt","w")
            f.write(str(summerized_text.encode("ascii","ignore")))
            f.close()
        else:
            summerized_text=main3.text_summary(articleText,sentNumber)
            posts.insert_one({"article":summerized_text})
            f=open("summ.txt","w")
            f.write(str(summerized_text.encode("ascii","ignore")))
            f.close()
        return render_template("submit.html",sum_text=summerized_text)

@app.route("/sendmail",methods=["POST"])
def mailADD():
    mailADD = request.form["mailADD"]
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.starttls()
    email = EMAIL
    password = PASSWORD
    smtp_object.login(email, password)
    from_add = email
    to_add = [mailADD]
    subject = "Here is your Article's Summary"
    with open("summ.txt", "r+") as f:
        message = f.read()
        f.truncate(0)
        f.close()
    message = message[2:-1]
    msg = 'Subject: {}\n\n{}'.format(subject, message)
    smtp_object.sendmail(from_add, to_add, msg)
    smtp_object.quit()
    return render_template("emailsent.html", emailadd=to_add[0])

@app.route("/history",methods=["POST"])
def history():

    lst = []
    count=0
    all_articles=posts.find()
    for art in all_articles:
        lst.append(art['article'])
    lst.reverse()
    return render_template('history.html',articles=enumerate(lst))
    



if __name__ == "__main__":
    app.run(debug=True)
