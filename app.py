from flask import Flask ,render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

import plotly
import plotly.express as px
import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'xxxxx'
app.config['MYSQL_DB'] = 'flaskMLApp'
mysql = MySQL(app)

@app.route('/')

def Index():

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Results')
    mysql.connection.commit()

    cur.execute('INSERT INTO Results (id,binaryResult,comments) VALUES(%s,%s,%s)',
                (1, 2, "You will receive a diagnostic once you fill in the form and press the button."))
    mysql.connection.commit()

    cur.execute('SELECT * FROM Results')
    data = cur.fetchall()
    return render_template('index.html' , Solutions=data)

@app.route('/input_health', methods=['POST'])
def healthCheck():

    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        chestPain = request.form['chestPain']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']

    # load model
    filename = 'HeartDisease_model.sav'
    dt = joblib.load(filename)


    predictionResult = dt.predict(
        [[float(age), float(sex), float(chestPain), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang),float(oldpeak),float(slope),float(ca),float(thal)]])
    print("Water potability : " + str(predictionResult[0]))

    if predictionResult[0] == 0 :
        resultDescription = "Diagnostic positive with an 80% of probability. Please contact your Health administration inmediately."
    else:
        resultDescription = "Diagnostic negative with an 80% of probability. Take care of your health like always."

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Results')
    mysql.connection.commit()
    cur.execute('INSERT INTO Results (id,binaryResult,comments) VALUES(%s,%s,%s)',
                (1, predictionResult[0], resultDescription))
    mysql.connection.commit()

    cur.execute('SELECT * FROM Results')
    data = cur.fetchall()
    
    return render_template('index.html', Solutions=data)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)


