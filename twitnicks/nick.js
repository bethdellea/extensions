var currTab = window.location.href;
console.log(currTab);
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
            var tweetAuth = $(".account-group .username", this).text();
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

//after document-load
$('#page-container').bind('DOMSubtreeModified',DOMModificationHandler);