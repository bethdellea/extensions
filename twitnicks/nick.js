//is this twitter or tweetdeck?? (or neither :o)
 chrome.tabs.query({active: true, currentWindow: true}, function(arrayOfTabs) {

     // since only one tab should be active and in the current window at once
     // the return variable should only have one entry
     var activeTab = arrayOfTabs[0];
     var activeTabId = activeTab.id; // or do whatever you need
	 alert(activeTab.url);
  });  //possibly can just do window.location.href for this...... will need to test and check when I'm not busy being a scardey cat

var nicks = {};
//load up saved data
chrome.storage.sync.get("twitNicData", function (nicArray) {
    console.log(nicArray);
	if(nicArray.isArray()){
		console.log("I'm an array!! do things withe me!!!");
		$.each(nicArray, function(username, nickname){
			nicks[username] = nickname;
			console.log("I just added" + username + " to the array under the alias " + nickname + "!!!");
		});
	}
});

if(!$.isEmptyObject(nickPairs)){
	//do replacement things,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


}