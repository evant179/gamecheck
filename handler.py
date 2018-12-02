from datetime import date, timedelta
import json
import os
import requests

apiKey = os.environ['GIANT_BOMB_API_KEY']
startTimeDelta = timedelta(days=1)
endTimeDelta = timedelta(days=7)


def processGameCheck(event, context):
    currentDate = date.today()
    startDate = currentDate + startTimeDelta
    endDate = currentDate + endTimeDelta

    print(f'Query for games between [{startDate}] and [{endDate}]')
    results = searchGames(startDate, endDate)
    # printGames(results)


def searchGames(startDate, endDate):
    url = 'https://www.giantbomb.com/api/releases'
    headers = {'user-agent': 'lambda-function'}
    fieldList = 'name,expected_release_day,expected_release_month,expected_release_year,release_date,platform'
    filter = f'release_date:{startDate:%Y-%m-%d}|{endDate:%Y-%m-%d}'
    sort = 'release_date:asc'
    payload = {
        'api_key': apiKey,
        'format': 'json',
        'field_list': fieldList,
        'filter': filter,
        'sort': sort
    }

    print(f'Request payload: {payload}')
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