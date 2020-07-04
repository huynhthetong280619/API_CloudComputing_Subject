# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import component, model
application = Flask(__name__)
CORS(application)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: component.sayHello()))

# Get temperature, humid current and next
def getTemperatureAndHumidityCN():
    current_temp = 0.0
    next_temp = 1.0
    current_humid = 85.0
    next_humid = 87.0
    modelTHCN = model.getTHCN()
    print(modelTHCN['currentTemp'])

    return jsonify({'currentTemprature':current_temp, 'predictTemprature':next_temp, 'currentHumid':current_humid, 'predictHumid':next_humid})
application.add_url_rule('/iot', 'getNextFromCurrent', (lambda: getTemperatureAndHumidityCN()))

# Get next temperature
def getNext(temperature):
    next_temp = temperature + 1.0
    return jsonify({'next':next_temp})
application.add_url_rule('/iot/<float:temperature>', 'getNext', (lambda temperature:
    getNext(temperature)))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    application.debug = True
    application.run(threaded=True, port=5000)