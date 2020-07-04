def getTHCN():
    return {
        'currentTemp' : 30,
        'predictTemp': 30.5,
        'currentHumidity': 87,
        'predictHumidity' : 86
    }

def getNT(temperature):
    return {'next': temperature+1.0}