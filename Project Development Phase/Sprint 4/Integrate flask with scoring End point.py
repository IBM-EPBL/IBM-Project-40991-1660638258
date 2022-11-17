import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "NqfwMRhDq1weTZdyqDwUGt4qs1bFR0A5qtW7cCc_Hk9D"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
#model = joblib.load('xg_RFR_forecast_model.sav')
#model = joblib.load('dec_model.sav')

@app.route('/')
def home():
    return render_template('intro.html')
@app.route('/predict')
def predict():
    return render_template('predict.html')
@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get('city')
    apikey="88d9c0f472a2dc46dc4a1f2d58f1d9d0"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey
    resp = requests.get(url)
    resp=resp.json()
    temp = str((resp["main"]["temp"])-273.15) +" °C"
    humid = str(resp["main"]["humidity"])+" %"
    pressure = str(resp["main"]["pressure"])+" mmHG"
    speed = str((resp["wind"]["speed"])*3.6)+" Km/hr"
    direc = str((resp["wind"]["deg"]))+" deg"
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed,direction = direc)   
@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[float(x) for x in request.form.values()]]
    print(x_test)
    # Deployed Link
    payload_scoring = {"input_data": 
			[{"field": [["Theoretical_Power", "Wind_Speed"]], 
			"values": x_test}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a5c5a088-a1bd-4beb-ab73-700e0d864e14/predictions?version=2022-11-15', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions =response_scoring.json()
    print(predictions)
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])


    pred =response_scoring.json()
    print(pred)
    #print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])

   # prediction = model.predict(x_test)
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))
    
   
if __name__ == "__main__":
    app.run(debug=False)