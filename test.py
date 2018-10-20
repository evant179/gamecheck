import json
import requests
import yaml

config = yaml.load(open("config.yaml"))
apiKey = config['apiKey']


def getReleaseDate(name):
    print('start request for: ' + name)
    url = 'https://www.giantbomb.com/api/search'
    headers = {'user-agent': 'test-script'}
    payload = {
        'api_key': apiKey,
        'format': 'json',
        'query': name,
        'resources': 'game',
        'field_list': 'name'
    }
    r = requests.get(url, headers=headers, params=payload)
    print('end request')

    data = json.loads(r.text)  # response comes back as str. convert to dict
    print(json.dumps(data, indent=2))


getReleaseDate("Red Dead")
