import whois
import re
import datetime
import requests
import argparse


DAYS_AMOUNT=30
HTTP_OK_STATUS_CODE=200


def parse_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_file',
                        help='enter the filepath to your text file with urls')
    return parser.parse_args()


def load_urls4check(path):
    with open(path, encoding='UTF-8') as data_file:
        return data_file.read()


def urls_separate(urls_list):
    return re.findall('.+', urls_list)


def is_server_respond_with_200(url):
    return requests.get(url).status_code == HTTP_OK_STATUS_CODE


def get_domain_expiration_date(url):
    return whois.whois(url).expiration_date[0] - datetime.datetime.today() > datetime.timedelta(days=DAYS_AMOUNT)


if __name__ == '__main__':
    parser = parse_path()
    path_to_urls = parser.path_to_file
    raw_urls = load_urls4check(path_to_urls)
    urls = urls_separate(raw_urls)
    for url in urls:
        if is_server_respond_with_200(url):
            print('Доменное имя {} отвечает на запрос статусом HTTP 200'.format(url))
        else:
            print('Доменное имя {} не отвечает на запрос статусом HTTP 200'.format(url))
        if get_domain_expiration_date(url):
            print('Доменное имя {} проплачено более чем на месяц'.format(url))
        else:
            print('Доменное имя {} проплачено менее чем на месяц'.format(url))