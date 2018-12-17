from datetime import date, timedelta
import json
import os
import requests

GIANT_BOMB_API_KEY = os.environ['GIANT_BOMB_API_KEY']
PASTEBIN_API_KEY = os.environ['PASTEBIN_API_KEY']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
TARGET_PHONE_NUMBERS = os.environ['TARGET_PHONE_NUMBERS']

START_TIME_DELTA = timedelta(days=1)
END_TIME_DELTA = timedelta(days=7)


def process_game_check(event, context):
    current_date = date.today()
    start_date = current_date + START_TIME_DELTA
    end_date = current_date + END_TIME_DELTA

    print(f'Query for games between [{start_date}] and [{end_date}]')
    games = search_games(start_date, end_date)
    converted_games = process_games(games)
    body = create_sms_body(converted_games)

    numbers = TARGET_PHONE_NUMBERS.split(',')
    for number in numbers:
        try:
            send_sms_message(body, number)
        except Exception as e:
            print(e)


def search_games(start_date, end_date):
    url = 'https://www.giantbomb.com/api/releases'
    headers = {'user-agent': 'lambda-function'}
    field_list = 'name,expected_release_day,expected_release_month,expected_release_year,release_date,platform'
    filter = f'release_date:{start_date:%Y-%m-%d}|{end_date:%Y-%m-%d}'
    sort = 'release_date:asc'
    payload = {
        'api_key': GIANT_BOMB_API_KEY,
        'format': 'json',
        'field_list': field_list,
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


def process_games(games):
    converted_games = set()

    for game in games:
        name = game['name']
        release_year = game['expected_release_year']
        release_month = game['expected_release_month']
        release_day = game['expected_release_day']
        platform = game['platform']
        platform_name = platform['name']

        if any(v is None for v in [release_year, release_month, release_day]):
            print(f'Skip game: {name}')
            continue

        release_date = date(release_year, release_month, release_day)
        game_info = f'{release_date:%D} | {name} | {platform_name}'
        converted_games.add(game_info)

    return sorted(converted_games)


def create_sms_body(converted_games):
    text = ''
    for game in converted_games:
        text += f'{game}\n'
    print(text)
    pastebin_link = create_pastebin(text)
    print(pastebin_link)

    raw_link = transform_to_raw_pastbin_link(pastebin_link)
    body = f"Here are this week's video game releases!\n{raw_link}"
    return body


def create_pastebin(text):
    url = 'https://pastebin.com/api/api_post.php'
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': text
    }
    response = requests.post(url, data=data)
    print(response)
    return response.text


def transform_to_raw_pastbin_link(link):
    index = link.find('m/')
    index += 1
    raw_link = link[:index] + '/raw' + link[index:]
    print(raw_link)
    return raw_link


def send_sms_message(body, target_phone_number):
    url = f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json'
    data = {
        'From': TWILIO_PHONE_NUMBER,
        'To': target_phone_number,
        'Body': body
    }
    response = requests.post(
        url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
    print(response)


if __name__ == "__main__":
    process_game_check('', '')
