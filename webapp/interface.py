from flask import Flask, session, render_template, request,make_response,redirect,flash
import sqlite3
import pandas as pd

questions=pd.read_excel("../Frågor/Frågor.xlsx")

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])

def select_questions():
    if request.method=="POST":
        inputFromForm=list(request.form.listvalues())
        conn = sqlite3.connect('../database.db')
        cursor = conn.execute("REPLACE INTO CURRENT_QUESTION(rowid, GAME_ID,QUESTION_ID,LEVEL) Values(1,1,"+str(inputFromForm[0][0])+","+str(inputFromForm[1][0]) +");")
        conn.commit()

    questionsPlusId=list(zip(questions["id"],questions["Fråga"]))
    return render_template("input.html",questionList=questionsPlusId )
