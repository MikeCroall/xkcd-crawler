# Python 3.5.1 tested
#
# If downloaded set is out of date, ie. does not contain most recent comic
# then the comics since most recently downloaded will be downloaded.
# If however the most recent comic is present, the script will scan all
# previous comics, ensuring ALL of them are present
#
# It is possible that script will need to run TWICE to ensure ALL comics
# are present, though this still maintains average case having optimal performance
#
# Script requires no user interaction from being started to self-termination


from os import listdir, makedirs
from os.path import exists, isfile, join
import requests as web
import urllib.request as image_downloader
from bs4 import BeautifulSoup

baseurl = 'http://xkcd.com/'
direc = 'images/'


def find_max_already_downloaded():
    only_files = [f for f in listdir(direc) if isfile(join(direc, f))]
    max_file_num = 0
    for file in only_files:
        n = int(file.split(' ')[0])
        if n > max_file_num:
            max_file_num = n
    return max_file_num


def detect_max_page():
    max_num_found = 1
    plain_text = web.get(baseurl).text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for a in soup.findAll('a', {}):
        link_no_slashes = a.get('href').replace('/', '')
        if link_no_slashes.isdigit():
            n = int(link_no_slashes)
            if n > max_num_found:
                max_num_found = n
    return max_num_found + 1 # plus 1 because link found is to previous comic


def img_spider(start_page, max_page):
    if start_page > max_page:
        print("Unusual start_page max_page combination...")
        print("Reverting to scanning all pages, starting at 1")
        start_page = 1
        
    page = start_page
    while page <= max_page:
        url = baseurl + str(page) + '/'
        plain_text = web.get(url).text
        soup = BeautifulSoup(plain_text, 'html.parser')
        for img in soup.findAll('img', {}):
            img_url = img.get('src')
            if 'comics' in img_url:
                filename = img_url.split('/')[-1].replace('_(1)', '')
                filepath = direc + '{} - '.format(page) + filename
                if exists(filepath):
                    print('{}/{} - Exists already - '.format(page, max_page) + filename)
                else:
                    print('{}/{} - Downloading... - '.format(page, max_page) + filename)
                    image_downloader.urlretrieve('http:' + img_url, filepath)
                break # to skip all imgs past the comic img, as we know we don't care
        page += 1


def scan_unseen_pages():
    if not exists(direc):
        makedirs(direc)

    start_page = 1 + find_max_already_downloaded()
    end_page = detect_max_page()

    print('Scanning from {} to {}...'.format(start_page, end_page))
    img_spider(start_page, end_page)
    print('Scan completed')


scan_unseen_pages()
