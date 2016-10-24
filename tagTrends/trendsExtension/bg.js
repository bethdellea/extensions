//document.getElementById('GNsubmit').addEventListener('click', neutralize);

//if we're on AO3 author page or IG user page (@ in the title of the page, along wiht url check)
//run the code --- if ig, get pic codes first, if AO3 just get uname and pseud

function getTagsA(){
    chrome.tabs.executeScript({file: 'a.js'});
    console.log("tag a executed");
}

function getTagsI(){
    chrome.tabs.executeScript({file: 'i.js'});
    console.log("tag i executed");
}

function checkUrl(urlIn){
    //is archiveofourown or instagram in it
    var ansA = urlIn.indexOf("archiveofourown");
    var ansI = urlIn.indexOf("instagram");
    if(ansA != -1){
        console.log("A is a go");
        getTagsA();
    }
    if(ansI != -1){
        console.log("I is a go");
        getTagsI();
    }
}

 
function callback(tabs){
    var currentTab = tabs[0];
    var currURL = currentTab.url;
    checkUrl(currURL);
    
}

function askTabs(tab){
    if (tab.status == "complete"){
    var query = {'active': true, 'currentWindow': true};

    chrome.tabs.query(query, callback);
    }
}

chrome.tabs.onUpdated.addListener(askTabs);
