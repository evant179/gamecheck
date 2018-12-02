from datetime import date, timedelta
import json
import os
import requests

apiKey = os.environ['GIANT_BOMB_API_KEY']
pastebin_api_key = os.environ['PASTEBIN_API_KEY']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_phone_number = os.environ['TWILIO_PHONE_NUMBER']
target_phone_numbers = os.environ['TARGET_PHONE_NUMBERS']
startTimeDelta = timedelta(days=1)
endTimeDelta = timedelta(days=7)


def processGameCheck(event, context):
    currentDate = date.today()
    startDate = currentDate + startTimeDelta
    endDate = currentDate + endTimeDelta

    print(f'Query for games between [{startDate}] and [{endDate}]')
    games = searchGames(startDate, endDate)
    convertedGames = processGames(games)
    body = createSmsBody(convertedGames)

    numbers = target_phone_numbers.split(',')
    for number in numbers:
        try:
            sendSmsMessage(body, number)
        except Exception as e:
            print(e)


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


def processGames(games):
    convertedGames = set()

    for game in games:
        name = game['name']
        releaseYear = game['expected_release_year']
        releaseMonth = game['expected_release_month']
        releaseDay = game['expected_release_day']
        platform = game['platform']
        platformName = platform['name']

        if any(v is None for v in [releaseYear, releaseMonth, releaseDay]):
            print(f'Skip game: {name}')
            continue

        releaseDate = date(releaseYear, releaseMonth, releaseDay)
        gameInfo = f'{releaseDate:%D} | {name} | {platformName}'
        convertedGames.add(gameInfo)

    return sorted(convertedGames)


def createSmsBody(convertedGames):
    text = ''
    for g in convertedGames:
        text += f'{g}\n'
    print(text)
    pasteBinLink = createPastebin(text)
    print(pasteBinLink)

    rawLink = transformToRawPastbinLink(pasteBinLink)
    body = f"Here are this week's video game releases!\n{rawLink}"
    return body


def createPastebin(text):
    url = 'https://pastebin.com/api/api_post.php'
    data = {
        'api_dev_key': pastebin_api_key,
        'api_option': 'paste',
        'api_paste_code': text
    }
    response = requests.post(url, data=data)
    print(response)
    return response.text


def transformToRawPastbinLink(link):
    index = link.find('m/')
    index += 1
    rawLink = link[:index] + '/raw' + link[index:]
    print(rawLink)
    return rawLink


def sendSmsMessage(body, targetPhoneNumber):
    url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
    data = {'From': from_phone_number, 'To': targetPhoneNumber, 'Body': body}
    response = requests.post(url, data=data, auth=(account_sid, auth_token))
    print(response)


if __name__ == "__main__":
    processGameCheck('', '')