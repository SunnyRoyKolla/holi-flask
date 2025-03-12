#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 15:30:15 2025

@author: sunnyroykolla
"""

from flask import Flask, render_template, request
import ephem
from datetime import datetime

app = Flask(__name__)

def calculate_correct_holi_date(year):
    """
    Finds the correct Holi date by checking the last full moon before Chaitra month.
    """
    # Get the full moons in February, March, and April
    feb_full_moon = ephem.previous_full_moon(f"{year}/3/1")
    march_full_moon = ephem.next_full_moon(f"{year}/3/1")
    april_full_moon = ephem.next_full_moon(f"{year}/4/1")

    # Convert dates to datetime format
    feb_date = datetime.strptime(str(feb_full_moon), "%Y/%m/%d %H:%M:%S")
    march_date = datetime.strptime(str(march_full_moon), "%Y/%m/%d %H:%M:%S")
    april_date = datetime.strptime(str(april_full_moon), "%Y/%m/%d %H:%M:%S")

    # Holi is celebrated on the full moon that falls before Chaitra month starts
    if feb_date.month == 2 and feb_date.day > 20:  # Late February case
        return feb_date.strftime("%B %d, %Y")
    elif march_date.month == 3:  # Normal March case
        return march_date.strftime("%B %d, %Y")
    else:  # If the correct full moon is in early April
        return april_date.strftime("%B %d, %Y")

@app.route("/", methods=["GET", "POST"])
def index():
    holi_date = ""  # Default empty
    if request.method == "POST":
        year = request.form.get("year")
        if year:
            holi_date = calculate_correct_holi_date(int(year))  # Calculate Holi date correctly
    return render_template("holi.html", holi_date=holi_date)

if __name__ == "__main__":
    app.run(debug=True)