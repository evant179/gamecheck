import handler

def capital_case(x):
    return x.capitalize()

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'

def test_transform_to_raw_pastbin_link():
    link = 'https://pastebin.com/test'
    raw_link = handler.transformToRawPastbinLink(link)
    print(f'{link} transformed to {raw_link}')
    assert raw_link == 'https://pastebin.com/raw/test'