# -*- coding: utf-8 -*-
# scrape status tool to get metadata from LEGACY site so we can create dataset and upload using JSON API
from bs4 import BeautifulSoup
import requests
from config import config
from configparser import ConfigParser


def get_metadata(trans_id):
    # legacy site.
    url = 'https://status.datahub.pnl.gov/view/' + str(trans_id)

    # read config file
    parser = ConfigParser()
    parser.read('connections.ini')
    legacy_datahub = parser['legacy_datahub']
    stat_user = legacy_datahub['stat_user']
    stat_pswrd = legacy_datahub['stat_pswrd']

    # get html document
    raw_req = requests.get(url, verify=False, timeout=10,
                           auth=(stat_user, stat_pswrd))
    # print(raw_req.status_code)
    # parse request
    pars_req = BeautifulSoup(raw_req.content, 'html.parser')
    # look for class
    metadata_html = pars_req.find(class_='left')

    fd_array = []
    if metadata_html is not None:
        fd_array.append(str(metadata_html.text))
    # print(fd_array)

    res = []
    if len(fd_array) != 0:
        for sub in fd_array:  # multiple strings returned so separate out
            res.append(sub.replace('\n', ''))
        results = ' '.join([str(x) for x in res])

        # i am using Instrument Name as dataset title
        # I need to extract the title. This was a quick way to do that (assuming Project ID always follows Instrument name...)
        left = 'Instrument Name'
        right = 'Project ID'
        title = results[results.index(left)+len(left):results.index(right)]
        print(f'Success! Metadata generated for {trans_id}, title: {title}')
    # we only use complete or released datasets so this else statement may not be necessary
    else:
        print(f'No metadata returned for {trans_id}')
        results = []
        title = []

    return results, title


if __name__ == '__main__':
    get_metadata(trans_id)
