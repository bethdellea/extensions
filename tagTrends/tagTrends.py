#Author: Beth Dellea
# August 2016
# collect and sort the tags frequently used by an account to show (recent) trends
# Version 1 to work with AO3 because they mark their tags nicely



def getPage(uname, pseud, pNum):
    #http://archiveofourown.org/users/uname/pseuds/pseud/works?page=pNum
    return("I am a page")


def getNumWorksPages(worksPg):
    numWorksPages = 2
    #do real parsing here to find that out
    return numWorksPages

def justWorks(workPg):
    #cut the text down to just the works section, perhaps just the tags for each
    #tbd based on effort for later things tbh
    onlyWork = workPg
    return onlyWork

def tagDict(worksList):
    #make a dictionary of each tag and number of times used
    #make sure to ignore capitalization
    tagDict = {"hi":2}
    return tagDict

def main():
    uname = input("Enter the username to check: ")
    pseud = input("Enter the pseudonym to check: ")
    workPg = getPage(uname, pseud, 1)
    numPgs = getNumWorksPages(workPg)
    workPg = justWorks(workPg)
    if numPgs > 1:
        for pNum in range(2, numPgs+1):
            currPg = getPage(uname, pseud, pNum)
            workPg += justWorks(currPg)
    tagsUsed = tagDict(workPg)
    print(tagsUsed)
    
















main()


    
