import pandas as pd
import os
from flask import Flask, render_template, request, redirect, url_for, abort, Response
import joblib
from werkzeug.utils import secure_filename


app = Flask(__name__)
model = joblib.load(open('model.pkl', 'rb'))

app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['UPLOAD_PATH'] = 'static/files/'

@app.route('/')
def home():
    print("home")
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    print("predict")
    uploaded_file = request.files['file']
    print("file uploaded")
    filename = secure_filename(uploaded_file.filename)

    print(filename)

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    d = {}
    with open(os.path.join(app.config['UPLOAD_PATH'], filename)) as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val

    input = [float(i) for i in d.values()]
    

    prediction = model.predict([input])
    output = prediction[0]

    return render_template('results.html',predicted_image='Prediction Result: {}'.format(output))


if __name__=="__main__":
    app.debug = True
    app.run()