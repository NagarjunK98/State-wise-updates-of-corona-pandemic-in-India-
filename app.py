from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup

link = 'https://www.mohfw.gov.in/'
req = requests.get(link)
soup = BeautifulSoup(req.content, "html.parser")

thead = soup.find_all('thead')[-1]
head = thead.find_all('tr')

tbody = soup.find_all('tbody')[-1]
body = tbody.find_all('tr')
body_rows = []

head_rows=['S. No.','Name of state/UT','Total Confirmed cases ','Cured/Discharged/Migrated','Death']

for tr in body:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    body_rows.append(row)

# print(head_rows)

df = pd.DataFrame(body_rows[:len(body_rows) - 2], columns=head_rows)
df.set_index(['S. No.'], inplace = True)
app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)



if __name__ == '__main__':
    app.run(debug=True)