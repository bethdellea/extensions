var currTab = window.location.href;
var isTweetdeck = false;
if(currTab.search("tweetdeck") != -1){
    isTweetdeck = true;
}

//do need to set things up to also run on page loads/document changes, since twitter likes to ajax things in and also because it's good to cover bases
  
  
//load up saved data
//will happen on initial page load...
function getNicks(){
    chrome.storage.sync.get("twitNicData", processNics);
}

function processNics(nickPairs){
    if(!$.isEmptyObject(nickPairs)){
		var pairedNics = JSON.parse(nickPairs["twitNicData"]);
        if(!$.isEmptyObject(pairedNics)){
	        //do replacement things,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
            $.each(pairedNics, function(username, nickname){
                sortOutTweets(nickname, username);
            });
        }
	}
}

function sortOutTweets(nick, handle){
    handle = "@" + handle;
    $("div.tweet").each(function(){
        if(!$(this).hasClass("nickProcessed")){
            var tweetAuth = "no one yet";
            if(!isTweetdeck){
                tweetAuth = $(".account-group .username", this).text();
            } else{
                tweetAuth = $(".account-inline .username", this).text();
            }
            if(tweetAuth == handle){
                var dispName = $(".fullname",this).text();
                dispName += " (" + nick +")";
                $(".fullname", this).text(dispName);
                $(this).addClass("nickProcessed"); 
            }
        }
       
    }); 
}

getNicks();

function DOMModificationHandler(){
    $(this).unbind('DOMSubtreeModified');
    setTimeout(function(){
        getNicks();
        $('#page-container').bind('DOMSubtreeModified',DOMModificationHandler);
    },2000);
}

function DOMModificationHandlerTD(){
    $(this).unbind('DOMSubtreeModified');
    setTimeout(function(){
        getNicks();
        $('.js-column').bind('DOMSubtreeModified',DOMModificationHandler);
    },2000);
}



$(document).ready(function(){


    //after document-load
    $('#page-container').bind('DOMSubtreeModified',DOMModificationHandler);
    if(isTweetdeck){
        $('.scroll-v').bind('DOMSubtreeModified',DOMModificationHandlerTD);
    }
});
