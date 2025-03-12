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

def calculate_holi_date(year):
    """
    Finds the correct Holi date based on the full moon in Phalguna month.
    """
    # Get the full moons in February, March, and April
    feb_full_moon = ephem.previous_full_moon(f"{year}/3/1")
    march_full_moon = ephem.next_full_moon(f"{year}/3/1")
    april_full_moon = ephem.next_full_moon(f"{year}/4/1")

    # Convert dates to readable format
    feb_date = datetime.strptime(str(feb_full_moon), "%Y/%m/%d %H:%M:%S")
    march_date = datetime.strptime(str(march_full_moon), "%Y/%m/%d %H:%M:%S")
    april_date = datetime.strptime(str(april_full_moon), "%Y/%m/%d %H:%M:%S")

    # Check where Phalguna Purnima falls
    if feb_date.month == 2 and feb_date.day > 20:
        return feb_date.strftime("%B %d, %Y")
    elif march_date.month == 3:
        return march_date.strftime("%B %d, %Y")
    else:
        return april_date.strftime("%B %d, %Y")

@app.route("/", methods=["GET", "POST"])
def index():
    holi_date = ""
    response_text = "Holi Falls on:"
    selected_year = None  # Default is None

    if request.method == "POST":
        year = request.form.get("year")
        if year:
            selected_year = int(year)  # Store selected year
            holi_date = calculate_holi_date(selected_year)
            
            # Determine if Holi is in the past or future
            today_year = datetime.now().year
            if selected_year < today_year:
                response_text = "Holi Fell on:"
            else:
                response_text = "Holi Falls on:"

    return render_template("holi.html", holi_date=holi_date, response_text=response_text, selected_year=selected_year)

if __name__ == "__main__":
    app.run(debug=True)