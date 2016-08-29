#Author: Beth Dellea
# August 2016
# collect and sort the tags frequently used by an account to show (recent) trends
# Version 1 to work with AO3 because they mark their tags nicely

import requests
import http.cookiejar
from bs4 import BeautifulSoup
import re
import os
import time
import random
import math


DEFINITELY_CHROME = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/45.0.2454.85 Safari/537.36"}

class HTTPResponseError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

def getTagText(tag):
    if tag is None:
        return ""
    tagStr = str(tag)
    soup = BeautifulSoup(tagStr, "html.parser")
    text = soup.get_text()
    return text
    

'''gets the number of works from the h2 which declares it, if it exists'''
def getNumFromWorks(h2):
    if h2 is None:
        return 0
    hStr = str(h2)
    soup = BeautifulSoup(hStr, "html.parser")
    text = soup.get_text()
    textList = text.split()
    numWorks = int(textList[-4])
    return numWorks
    
'''requests and catches the desired user works page on ao3'''
def getPage(uname, pseud, pNum):
    #http://archiveofourown.org/users/uname/pseuds/pseud/works?page=pNum
    profileURL = "http://archiveofourown.org/users/"+uname+"/pseuds/"+pseud+"/works?page="+str(pNum)
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME)
    return(rget.text)

'''isolates the number of pages of works for the user
takes the number of works and then figures out the number of pages based on 20 works/page'''
def getNumWorksPages(worksPg):
    pgSoup = BeautifulSoup(worksPg, "html.parser")
    worksBody = pgSoup.find("div",  {"id": "main"})
    if worksBody is None: #if you can't find the number of works, there is only one page
        return 1
    worksHead = worksBody.find("h2", "heading")
    numWorks = getNumFromWorks(worksHead)
    if numWorks <= 20: #ao3 displays 20 works per page, will not say number of works if only one page is necessary
        return 1
    numWorksPages = math.ceil(numWorks/20) #if 20 works/page, any extras will be on the next one

    return numWorksPages

'''gets the freeform tags from a page and discards the rest of the html'''
def justTags(workPg):
    #cut the text down to just the works section, perhaps just the tags for each
    #tbd based on effort for later things tbh
    pgSoup = BeautifulSoup(workPg, "html.parser")
    freeform = pgSoup.find_all("li", "freeforms")
    onlyTags = []
    for tag in freeform:
        onlyTags.append(getTagText(tag))
    return onlyTags

'''makes a dictionary of tags used and the number of times each has been used'''
def tagDict(tagsList):
    #make a dictionary of each tag and number of times used
    #make sure to ignore capitalization
    tagDict = {}
    for tag in tagsList:
        tag = tag.lower()
        if tag not in tagDict:
            tagDict[tag] = 1
        else:
            tagDict[tag] = tagDict[tag] + 1
    return tagDict

def topTags(sortedDict):
    if len(sortedDict) < 15:
        #work with what's been given
        topTags = sortedDict
    else:
        #grab the top 15 most used tags for an author
        topTags = sortedDict[0:14]
    return topTags

def tagsNoFreq(topTags):
    
    tagsList = []
    for tag in topTags:
        tagsList.append(tag[1])
    print(tagsList)
    

def main():
    uname = input("Enter the username to check: ")
    pseud = input("Enter the pseudonym to check: ")
    workPg = getPage(uname, pseud, 1)
    numPgs = getNumWorksPages(workPg)
    freeformTags = justTags(workPg)
    if numPgs > 1:
        for pNum in range(2, numPgs+1):
            currPg = getPage(uname, pseud, pNum)
            freeformTags += justTags(currPg)

    tagsUsed = tagDict(freeformTags)
    newOrder = sorted([(value,key) for (key,value) in tagsUsed.items()], reverse=True)   #http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    tops = topTags(newOrder)
    printable = tagsNoFreq(tops)












main()


    
