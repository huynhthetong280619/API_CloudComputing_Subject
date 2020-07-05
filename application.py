# app.py
from flask import Flask, jsonify
from firebase import firebase
application = Flask(__name__)

URL = 'https://project-cloud-e7988.firebaseio.com'
DATABASE = 'Nhom7/DHT11/'

PARAMETERS_URL = 'https://cloud-abc-cea03.firebaseio.com'
PARAMETERS_DATABASE = '/ABC'

def Index():
    return 'API Temperature.'
application.add_url_rule('/', 'index', (lambda: Index()))

# Get temperature, humid current and predict
def getTemperatureAndHumidity():

    fb = firebase.FirebaseApplication(URL)
    res = fb.get(DATABASE, None)
    data = list(res.values())
    temperature = float(data[len(data)-1]['Temperature'])
    humidity = float(data[len(data)-1]['Humidity'])

    return jsonify({'currentTemprature': temperature,
                    'currentHumid':humidity
                    })

application.add_url_rule('/iot', 'getTemperatureAndHumidity', (lambda : getTemperatureAndHumidity()))

# Get predict temperature base on temperature and humidity
def getPredictTemperature(temperature, humidity):
    res=getTemperatureHours(temperature, humidity)
    return jsonify({'next': res})

application.add_url_rule('/iot/<float:temperature>/<float:humidity>',
    'getPredictTemperature', (lambda temperature, humidity:
    getPredictTemperature(temperature, humidity)))

def getTemperatureHours(temp, humid):
    fb = firebase.FirebaseApplication(PARAMETERS_URL)
    res = fb.get(PARAMETERS_DATABASE, None)
    data = list(res['1H'].values())
    A = data[0]
    B = data[1]
    C = data[2]
    res = round(float(A*temp + B*humid + C), 1)
    return res

def getPredictTemperatureNext():
    fb = firebase.FirebaseApplication(URL)
    res = fb.get(DATABASE, None)
    data = list(res.values())
    temperature = float(data[len(data)-1]['Temperature'])
    humidity = float(data[len(data)-1]['Humidity'])
    return jsonify({'next':getTemperatureHours(temperature, humidity)})
application.add_url_rule('/iot/next','getPredictTemperatureNext',
           lambda:getPredictTemperatureNext())  

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    application.debug = True
    application.run(threaded=True, port=5000)
