//is this twitter or tweetdeck?? (or neither :o)

 //chrome.tabs.onActivated.addListener(function(evt){ 
/*
 chrome.tabs.query({active: true, currentWindow: true}, function(arrayOfTabs) {

     // since only one tab should be active and in the current window at once
     // the return variable should only have one entry
     var activeTab = arrayOfTabs[0];
     var activeTabId = activeTab.id; // or do whatever you need
	 //if(activeTab.url.indexOf("twitter.com") > -1){
		alert("a twit page");
		alert(activeTab.url);
		//}
  });  //possibly can just do window.location.href for this...... will need to test and check when I'm not busy being a scardey cat
*/

var currTab = window.location.href;
//alert(currTab);
//currently unnecessary check due to the things going on in manifest.json
 
//do need to set things up to also run on page loads/document changes, since twitter likes to ajax things in and also because it's good to cover bases
  
  
//load up saved data
//var nickPairs = JSON.parse(localStorage.getItem("twitNicData"));
chrome.storage.sync.get("twitNicData", processNics);
	//var nicks = {};
function processNics(nickPairs){
	
	if(!$.isEmptyObject(nickPairs)){
		var pairedNics = JSON.parse(nickPairs["twitNicData"]);
		console.log("I'm an thing!! do things withe me!!!");
		$.each(pairedNics, function(username, nickname){
			console.log("I just processed " + username + " to the array under the alias " + nickname + "!!!");
		});
	}

if(!$.isEmptyObject(pairedNics)){
	//do replacement things,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


}

}