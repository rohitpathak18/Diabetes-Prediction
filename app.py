# Importing essential libraries
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import argparse
import numpy as np
import pickle

model = pickle.load(open('diabetes Prediction.pkl','rb'))
app = Flask(__name__)

def predict():
    df = input_group("Diabetes Prediction",[
    input('Glucose(mg/dL)', name='glucose', placeholder="e.g. 120",type=NUMBER),
    input('Insulin(IU/mL)', name='insulin', placeholder="e.g. 94",type=NUMBER),
    input('Body Mass Index(kg/m2)', name='bmi', placeholder="e.g. 52",type=NUMBER),
    input('Age', name='age', placeholder="e.g. 23", type=NUMBER),
    ])

    glucose = df['glucose']
    insulin = df['insulin']
    bmi = df['bmi']
    age = df['age']

    fetch_data = np.array([[glucose, insulin, bmi, age]])
    my_prediction = model.predict(fetch_data)
    if my_prediction == 0:
        result = "Great! You DON'T have diabetes."
        put_success(result)
        put_html('<img src="https://media0.giphy.com/media/TGQyLdzYv90FjplXkr/giphy.gif">')
    if my_prediction == 1:
        result = "Oops! You Have Diabetes"
        put_warning(result)
        put_html('<img src="https://media4.giphy.com/media/1k1ytTA4AHJnp7OvUJ/giphy.gif">')


app.add_url_rule('/tool','webio_view',webio_view(predict), methods=['GET','POST','OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)

#app.run(host='localhost',port=80)