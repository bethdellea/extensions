chrome.tabs.executeScript({ file: 'jquery-2.1.3.js'}); 
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
    //RE with urlIn to check for A or I
    var urlPieces = urlIn.split("/");
    
    console.log(urlPieces);
}

 var query = {active: true, currentWindow: true};
function callback(tabs){
    var currentTab = tabs[0];
    var currURL = currentTab.url;
    var curr = checkUrl(currURL);
    if( curr == "a"){
        getTagsA();
    }
    if(curr == "i"){
        getTagsI();
    }
}

chrome.tabs.query(query, callback);