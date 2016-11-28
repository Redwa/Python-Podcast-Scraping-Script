# This is the original (unedited) version, written by Michael Kennedy (Talk Python To Me)
# Use this to download 3 episodes from the pythonbytes link
# Runs in Python 3 | Needs requests package  

import requests
import sys
import os
from xml.etree import ElementTree

def main():
    rss_url = 'https://pythonbytes.fm/episodes/rss' # Edit this to change target

    resp = requests.get(rss_url)
    if resp.status_code != 200:
        print("ERROR: {}".format(resp.status_code))
        return

    xml_text = resp.text
    xml = ElementTree.fromstring(xml_text)
    
    items = xml.findall('channel/item')
    print("Downloading {} episodes...".format(len(items)))
    for item in items:
        url = item.find('enclosure').attrib.get('url')
        title = item.find('title').text
        print(title + " ... ", end='')
        sys.stdout.flush()
        # print(url)
        name = url.split('/')[-1]
        if os.path.exists(name):
            print("File {} already exists, skipping.".format(name))
            continue
        resp = requests.get(url, stream=True)
        with open(name, 'wb') as fout:
            for chunk in resp.iter_content(1024*32):
                fout.write(chunk)
        print("done.")


if __name__ == '__main__':
    main()
