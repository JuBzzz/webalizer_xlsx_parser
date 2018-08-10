import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import datetime
"""
This script downloads the monthly report pages from the Webalizer 2.0
http://www.webalizer.org/
"""



def get_links(html):
    '''
        On the /webstat page, the webalizer will list links to the last 12
        months of reports.
        The links are located in anchor elements with a href that starts with
        'usage'
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
        Given an adress, send a request and return the decoded response.
    '''
    site = urlopen(address)
    html = ""
    try:
        html = site.read().decode('utf-8')
    finally:
        # Clean up the site, even if it could not be loaded.
        site.close()
    return html


def download_stats(address, directory):
    '''
        Donwloads each report page listed on the /webstat page and store the
        html files into the given directory.
    '''
    raw_html = fetch_html(address)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    links = get_links(raw_html)
    today = datetime.date.today()

    for href in links:
        if (int(href[6:10]) < today.year or
            int(href[6:10]) == today.year and int(href[10:12]) != today.month):
            ## Checks if the page is from the previous year or if it is from
            #  this year, but on a previous month
            if not os.path.isfile('{}/{}'.format(directory, href)):
                ## Checks if the page has already been downloaded
                html = fetch_html(address + href)

                with open('{}/{}'.format(directory, href), 'w') as f:
                    f.write(html)
                    f.close()


if __name__ == '__main__':
    address = input("Type in the webstat address (http://www.website.com/plesk-stat/webstat/):")
    directory = input("Type in the target directory to save downloaded pages:")

    download_stats(address, directory)
