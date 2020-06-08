from flask import Flask, request, jsonify, render_template
import base64, json
from io import BytesIO
import numpy as np

# declare constants
HOST = '0.0.0.0'
PORT = 8889

# initialize flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict', methods=['GET','POST'])
def predict():
    results = {"prediction" :"Empty", "probability" :{}}

    # get data
    input_img = BytesIO(base64.urlsafe_b64decode(request.form['img']))

    # model.predict method takes the raw data and output a vector of probabilities
    res =  model.predict(input_img)

    results["prediction"] = str(CLASS_MAPPING[np.argmax(res)])
    results["probability"] = float(np.max(res))*100
    # results["prediction"] = 5
    # results["probability"] = 50.424

    # output data
    return json.dumps(results)

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,debug=True,  # automatic reloading enabled
            port=PORT)