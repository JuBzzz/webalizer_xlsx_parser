import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import datetime


def get_links(html):
    '''
        Looks for every <a> elements that points to a address that starts with
        'usage'. These addresses point to the pages which we want to download.
    '''
    soup = BeautifulSoup(html,  'html.parser')

    links = []
    for link in soup.find_all('a'):
        link = link.get('href')
        if link.startswith('usage'):
            links.append(link)

    return links


def fetch_html(address):
    '''
        Given a website adress, send a request and return the decoded response.
    '''
    site = urlopen(address)
    try:
        html = site.read().decode('utf-8')
    finally:
        site.close()
    return html


def destination_lookup(directory):
    '''
        Returns the destination directory, create one if it does not exist
    '''
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dest = '{}/{}'.format(current_dir, directory)
    if not os.path.isdir(dest):
        os.mkdir(dest)
    return dest


def download_stats(address, directory):
    '''
        Before downloading each page, checks if it has not been downloaded and
        if the date points to a date before the current month.
    '''
    raw_html = fetch_html(address)
    destination = destination_lookup(directory)
    links = get_links(raw_html)
    today = datetime.date.today()

    for href in links:
        if (int(href[6:10]) < today.year or
            int(href[6:10]) == today.year and int(href[10:12]) != today.month):
            if not os.path.isfile('{}/{}'.format(destination, href)):
                html = fetch_html(address + href)

                with open('{}/{}'.format(destination, href), 'w') as f:
                    f.write(html)
                    f.close()


if __name__ == '__main__':
    address = input("Type in the webstat address (http://www.website.com/plesk-stat/webstat/):")
    directory = input("Type in the directory to download the pages:")

    download_stats(address, directory)
