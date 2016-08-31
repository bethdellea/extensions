#Author: Beth Dellea
# August 2016
# collect and sort the tags frequently used by an account to show (recent) trends
# Version 1 to work with AO3 because they mark their tags nicely
# Currently breaks if a nonexistant username is entered. In full extension form this should not be an issue
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

def getTagTextAO3(tag):
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
    #print(textList)
    if len(textList) == 4:
        numWorks = int(textList[0])
    else:
        numWorks = int(textList[-4])
    return numWorks
    
'''requests and catches the desired user works page on ao3'''
def getPageAO3(uname, pseud, pNum):
    #http://archiveofourown.org/users/uname/pseuds/pseud/works?page=pNum
    profileURL = "http://archiveofourown.org/users/"+uname+"/pseuds/"+pseud+"/works?page="+str(pNum)
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME)
    return(rget.text)

'''requests and catches the desired profile page on instagram'''
def getPageInsta(uname):
    profileURL = "https://www.instagram.com/" + uname + "/"
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME)
    return(rget.text)

'''requests and catches the desired photo page on instagram'''
def getPicPg(photoCode):
    profileURL = "https://www.instagram.com/p/" + photoCode + "/"
    rget = requests.get(profileURL, headers=DEFINITELY_CHROME)
    return(rget.text)

'''Users have been putting their hashtags as comments a lot these days instead of in captions. Let's go to each picture and get them'''
def getPicIDS(page):
    #doesn't work on private accounts but individual photos are visible
    #can get pic ids in js and pass to the python program for further analysis!
    regx = re.compile('(?<="code": ").*?(?=", "date":)')
    picIDList = regx.findall(page) #will return a list! ;)
    return picIDList

'''returns a list of all hashtags used in photo comments by the user'''
def getCommentTags(page):
    picIDs = getPicIDS(page)
    tagList = []
    print(picIDs)
    for pic in picIDs:
        picPg = getPicPg(pic)
        regx = re.compile('(?<="text": ").*?(?=", "created_at":)')
        picComment = regx.findall(picPg) #will return a list! ;)
        for comment in picComment:
            tagList += getTagFromText(comment)
    return tagList

'''isolates the number of pages of works for the user
takes the number of works and then figures out the number of pages based on 20 works/page'''
def getNumWorksPages(worksPg):
    pgSoup = BeautifulSoup(worksPg, "html.parser")
    worksBody = pgSoup.find("div",  {"id": "main"})
    worksHead = worksBody.find("h2", "heading")
    numWorks = getNumFromWorks(worksHead)
    if numWorks == 0:
        return 0
    elif numWorks <= 20: #ao3 displays 20 works per page, will not say number of works if only one page is necessary
        return 1
    numWorksPages = math.ceil(numWorks/20) #if 20 works/page, any extras will be on the next one
    return numWorksPages


'''gets the freeform tags from a page and discards the rest of the html'''
def justTagsAO3(workPg):
    #cut the text down to just the works section, perhaps just the tags for each
    #tbd based on effort for later things tbh
    pgSoup = BeautifulSoup(workPg, "html.parser")
    freeform = pgSoup.find_all("li", "freeforms")
    onlyTags = []
    for tag in freeform:
        onlyTags.append(getTagTextAO3(tag))
    return onlyTags


'''gets the hashtags used in most recent post captions from the instagram caption'''
def justTagsInst(profPg):
    regx = re.compile('(?<="caption":).*?(?=, "likes":)')
    captionList = regx.findall(profPg) #will return a list! ;)
    tagList = []
    for caption in captionList:
        tagList += getTagFromText(caption)
    return tagList

'''isolate the hashtags, minus symbol, used in bodies of text'''
def getTagFromText(text):
    textWds = text.split()
    tagList = []
    for word in textWds:
        if word[0] == "#":
            word = word[1:]
            tagList.append(word)
    return tagList

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

'''grab the topNum most frequently used tags or all the tags that qualify,
if topNum is too high'''
def topTags(sortedDict, topNum):
    if len(sortedDict) < topNum:
        #work with what's been given
        topTags = sortedDict
    else:
        #grab the top 15 most used tags for an author
        topTags = sortedDict[0:topNum]
    return topTags

'''we have a tuple of frequency and tag. We return just the tag'''
def tagsNoFreq(topTags, src):
    tagsList = []
    for tag in topTags:
        currTag = tag[1]
        if src == "instagram":
            currTag = makeTagHashtag(currTag)
        tagsList.append(currTag)
    return tagsList

'''uses the instagram tag search base url'''
def makeTagLinkInsta(tag):
    baseURL = "https://www.instagram.com/explore/tags/"
    return baseURL + tag

'''for the #aesthetic on instagram''' 
def makeTagHashtag(tag):
    hashtag="#" + tag
    return hashtag

'''uses the ao3 tag search base url'''
def makeTagLinkAO3(tag):
    baseURL = "http://archiveofourown.org/tags/"
    tagNoSp = tag.split()
    fullURL = baseURL
    for i in range(0, len(tagNoSp)-1):
        fullURL += tagNoSp[i] + "%20"
    fullURL += tagNoSp[len(tagNoSp)-1] + "/works"
    return fullURL

'''takes a tag's text and its url and makes a functional href link out of it'''
def makeLiveLink(tag, url):
    linkCode = "<a href='" + url + "' target='_blank'>" + tag + "</a>"
    return linkCode

def printPretty(pseud, tagList):
    if len(tagList) > 0:
        print(pseud, "'s ", len(tagList), " Most Frequently Used Tags: ")
        tagpile = ""
        for tag in tagList:
            tagpile += tag
            tagpile += ", "
        tagpile = tagpile[:len(tagpile)-2]
        print(tagpile)
    else:
        print(pseud, " has no tags to show")
    

def main():
    src = input("Would you like to work with AO3 or instagram? ")
    pseud = ""
    if src == "AO3":
        topNum = 15
        uname = input("Enter the username to check: ")
        pseud = input("Enter the pseudonym to check: ")
        workPg = getPageAO3(uname, pseud, 1)
        numPgs = getNumWorksPages(workPg)
        freeformTags = justTagsAO3(workPg)
        if numPgs > 1:
            for pNum in range(2, numPgs+1):
                currPg = getPageAO3(uname, pseud, pNum)
                freeformTags += justTagsAO3(currPg)
    elif src == "instagram":
        topNum = 5
        uname = input("Enter the username to check: ")
        pseud = uname
        picPage = getPageInsta(uname)
        commentTags = getCommentTags(picPage)
        freeformTags = justTagsInst(picPage)
        freeformTags = commentTags + freeformTags #should re-name this variable later

    tagsUsed = tagDict(freeformTags)
    newOrder = sorted([(value,key) for (key,value) in tagsUsed.items()], reverse=True)   #http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    tops = topTags(newOrder, topNum)
    #topTags needs an answer for if they're all used only once
    printable = tagsNoFreq(tops, src)
    printPretty(pseud, printable)
    






main()


    


