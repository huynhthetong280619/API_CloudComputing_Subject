# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import component, model
application = Flask(__name__)
CORS(application)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: component.sayHello()))

# Get temperature, humid current and predict
def getTemperatureAndHumidityCN():
    modelTHCN = model.getTHCN()
    return jsonify({'currentTemprature':modelTHCN['currentTemp'], 'predictTemprature': modelTHCN['predictTemp'], 'currentHumid':modelTHCN['currentHumidity'], 'predictHumid':modelTHCN['predictHumidity']})
application.add_url_rule('/iot', 'getNextFromCurrent', (lambda: getTemperatureAndHumidityCN()))

# Get next temperature
def getNext(temperature):
    modelNext = model.getNT(temperature)
    return jsonify({'next':modelNext['next']})

application.add_url_rule('/iot/<float:temperature>', 'getNext', (lambda temperature:
    getNext(temperature)))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    application.debug = True
    application.run(threaded=True, port=5000)