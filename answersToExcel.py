#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 20:00:47 2021

@author: hakanbernhardsson
"""

import pandas as pd
import sqlite3

fragor=pd.read_excel("Frågor/Frågor.xlsx")
svar=pd.read_excel("Svar/Svar.xlsx")


conn = sqlite3.connect('test.db')
svar = pd.read_sql_query("SELECT * from ANSWERS",conn)
#cursor = conn.execute("SELECT * from ANSWERS")
print(svar)

svar=svar.merge(fragor,how="left", left_on="QUESTION_ID", right_on="id")
svar=svar[["QUESTION_ID", "USERNAME", "Fråga namn", "Fråga", "GUESS", "Svar","LEVEL","TIMESTAMP"]]
svar["value"]=0

svar.loc[(svar.GUESS==svar.Svar),"value"]=1
svar["value"]=svar["value"]*svar["LEVEL"]

svar.to_excel("RattadRad.xlsx")
