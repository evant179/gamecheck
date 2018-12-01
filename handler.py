import json
import requests
import os

apiKey = os.environ['GIANT_BOMB_API_KEY']


def processGameCheck(event, context):
    results = searchGames('super mario')
    # printGames(results)


def searchGames(name):
    url = 'https://www.giantbomb.com/api/releases'
    headers = {'user-agent': 'lambda-function'}
    fieldList = 'name,expected_release_day,expected_release_month,expected_release_year,release_date,platform'
    filter = 'release_date:2018-12-15 00:00:00|2018-12-31 00:00:00'
    sort = 'release_date:asc'
    payload = {
        'api_key': apiKey,
        'format': 'json',
        'query': name,
        'resources': 'game',
        'field_list': fieldList,
        'filter': filter,
        'sort': sort
    }
    r = requests.get(url, headers=headers, params=payload)

    # response comes back as str. convert to dict
    response = json.loads(r.text)
    # print(json.dumps(response, indent=2))  # pretty print json string
    print(json.dumps(response))
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


if __name__ == "__main__":
    processGameCheck('', '')