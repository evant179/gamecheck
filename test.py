import requests
import yaml

config = yaml.load(open("config.yaml"))

def getReleaseDate(name):
    print('start request for: ' + name)
    print(config['apiKey'])
    print('end request')


getReleaseDate("Red Dead Redemption 2")
