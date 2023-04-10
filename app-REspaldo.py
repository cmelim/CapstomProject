'''
from flask import Flask, jsonify, request

app = Flask(__name__)

import joblib
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict(data)
    return jsonify(prediction.tolist())
#import joblib
'''

from flask import Flask, render_template, request,  redirect, url_for
import joblib
import os
from os.path import join, dirname, realpath




app = Flask(__name__)
#model = joblib.load('model.pkl')

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


@app.route('/')
def home():
    #return render_template('form.html')
    return render_template('uploadFile.html')
'''
@app.route('/predict', methods=['POST'])
def predict():
    input_data = [float(x) for x in request.form.values()]
    #prediction = model.predict([input_data])
    prediction = "Caca ~!"
    return render_template('result.html', prediction )
'''

@app.route('/predict', methods=['POST'])
def predict():
    input_data = [float(x) for x in request.form.values()]
    #prediction[] = "Caca" #model.predict([input_data])
    prediction= ["Caca", "Volvo", "BMW"] 
    return render_template('result.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)