from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import json

# Creating First URL

URL = "https://simple.wikipedia.org/wiki/Climate_change"
internal_urls = []
count = 1

# Extracting the HTML document from the given url
def getHTMLdocument(url):
    page = requests.get(url)
    # response will be provided in JSON format
    return BeautifulSoup(page.text, 'html.parser')

# Collecting Internal Links

def internal_links(soup, site):
    internallinks = []
    int_pattern = re.compile("^(/)")
    for link in soup.find_all("a",href=int_pattern):
        href=link.get('href')
        if href:
            if link.attrs['href'] not in internallinks:
                if(link.attrs['href'].startswith('/')):
                    internallinks.append(site+link.attrs['href'])
                    if link.attrs['href'] not in internal_urls:
                        internal_urls.append(site+link.attrs['href'])
                        
                else:
                    internallinks.append(link.attrs['href'])
    return len(internallinks)

# Collecting External Links

def external_links(soup, site):
    externallinks = []
    ext_pattern = re.compile("^(http|www)")
    for link in soup.find_all('a', href=ext_pattern):
        href=link.get('href')
        if href:
            if link.attrs['href'] not in externallinks:
                externallinks.append(link.attrs['href'])
    return len(externallinks)

# Collecting Reference Links

def reference_links(soup):
    referencelinks = []
    for link in soup.find_all('a', href = re.compile("^(#)")):
        href=link.get('href')
        if href:
            if link.attrs['href'] not in referencelinks:
                referencelinks.append(href)
    return len(referencelinks)

# Getting the timestamp from latest modified value

def time_stamp(soup):
    timestamp = []
    check = soup.find("script", {"type":"application/ld+json"})
    if check is not None:
        data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
        timestam = data['dateModified']
        #print(timestam)
        timestam = timestam.strip("[]")
        if timestam:
            timestamp.append(timestam)
        else:
            timestamp.append("None")
    else:
        timestamp.append("None")
    return timestamp

# Collect all data

def links(URL):
    content=getHTMLdocument(URL)
    len_internallink = internal_links(content, URL)
    len_externallinks = external_links(content, URL)
    len_referencelinks= reference_links(content)
    timestamp=time_stamp(content)
    
    return (len_internallink,len_externallinks,len_referencelinks,timestamp)

# Create a Dataframe with the data collected

info = links(URL)
data = pd.DataFrame(columns=['PageCount','INTcount','EXTcount','URLfragments','timestamp'])
data.loc[0] = [1, info[0], info[1], info[2], info[3]]

for url in range(199):
    count += 1
    currentURL = internal_urls[url]
    urlData = links(currentURL)
    row = {'PageCount': count, 'INTcount':urlData[0], 'EXTcount':urlData[1], 'URLfragments':urlData[2],'timestamp':urlData[3]}
    data = data.append(row, ignore_index=True)

print(data.head(200))
data.to_csv('dataset2.csv')




