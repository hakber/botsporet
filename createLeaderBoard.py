#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 00:00:07 2021

@author: hakanbernhardsson
"""

import pandas as pd

fragor=pd.read_excel("Frågor/Frågor.xlsx")
rattadRad=pd.read_excel("RattadRad.xlsx")


rattadRad=rattadRad[["USERNAME","value","Fråga namn"]]

leaderBoard=rattadRad.pivot(index="USERNAME", columns='Fråga namn', values="value")

fragaOrdning=fragor["Fråga namn"].tolist()
fragaOrdning=fragaOrdning[:len(leaderBoard.columns)]

leaderBoard=leaderBoard[ fragaOrdning ]
leaderBoard["sum"]=leaderBoard.sum(axis=1, numeric_only=True)
leaderBoard=leaderBoard.sort_values(by=["sum"], ascending=False)

leaderBoard.to_excel("Leaderboard.xlsx")
