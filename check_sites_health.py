import whois
import re
import datetime
import requests


DAYS_AMOUNT=30


def load_urls4check(path):
    with open(path, encoding='UTF-8') as data_file:
        return data_file.read()


def make_urls_great_again(data):
    return re.findall('.+', data)


def is_server_respond_with_200(url):
    return requests.get(url).status_code == 200


def get_domain_expiration_date(url):
    return whois.whois(url).expiration_date[0] - datetime.datetime.today() > datetime.timedelta(days=DAYS_AMOUNT)


if __name__ == '__main__':
    data = load_urls4check(input('Введите путь до текстового файла с URL адресами: '))
    urls = make_urls_great_again(data)
    for url in urls:
        if is_server_respond_with_200(url):
            print('Доменное имя {} отвечает на запрос статусом HTTP 200'.format(url))
        else:
            print('Доменное имя {} не отвечает на запрос статусом HTTP 200'.format(url))
        if get_domain_expiration_date(url):
            print('Доменное имя {} проплачено более чем на месяц'.format(url))
        else:
            print('Доменное имя {} проплачено менее чем на месяц'.format(url))