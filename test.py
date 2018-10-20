import json
import requests
import yaml

config = yaml.load(open("config.yaml"))
apiKey = config['apiKey']


def searchGames(name):
    url = 'https://www.giantbomb.com/api/search'
    headers = {'user-agent': 'test-script'}
    fieldList = 'name,expected_release_day,expected_release_month,expected_release_year'
    payload = {
        'api_key': apiKey,
        'format': 'json',
        'query': name,
        'resources': 'game',
        'field_list': fieldList
    }
    r = requests.get(url, headers=headers, params=payload)

    response = json.loads(
        r.text)  # response comes back as str. convert to dict
    # print(json.dumps(response, indent=2)) # pretty print json string
    return response['results']


def printGames(games):
    for game in games:
        name = game['name']
        month = 'NA' if not game['expected_release_month'] else game[
            'expected_release_month']
        day = 'NA' if not game['expected_release_day'] else game[
            'expected_release_day']
        year = 'NA' if not game['expected_release_year'] else game[
            'expected_release_year']
        date = str(month) + '/' + str(day) + '/' + str(year)
        print('[' + name + '] - [' + date + ']')


results = searchGames("Red Dead")
printGames(results)
