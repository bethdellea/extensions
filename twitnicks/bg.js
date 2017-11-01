//chrome.tabs.executeScript({ file: 'jquery-2.1.3.js'}); 
document.getElementById('addFields').addEventListener('click', addFields);

 function addFields(){
	$fieldHTML = "<div class='row'>
					<input type='text' name='handle' placeholder='username'>&emsp;&emsp;<input type='text' name='nick' placeholder='nickname'> &emsp;&emsp;&emsp; <a href='javascript();' class='remRow' onclick='remFields(this);'>x</a>
                </div> <!-- row -->";
	$("#formFields").append($fieldHTML);
 
 }
 
 function remFields(fieldRow){
		fieldRow.remove();
 }
  
  function saveAssoc(){
	//save username + nickname pairs in local storage, nick.js will pull from local storage to set up dict of needed pairs, etc etc
	var nickPairs = {};
	$(".row").each(function(){
		//TODO: clean input at least a little before you store -- probably simplest to just restrict it to twitter-accepted username charas and 
					//numbers + letters for username and nickname, respectively for v1
		var uname = $(this).find("handle").val();
		var nickname = $(this).find("nick").val();
		nickPairs[uname] = nickname;
	});
	
	if(nickPairs.length){
		//if we have entered data, save it!!
		chrome.storage.sync.set({"twitNicData": nickPairs});
	} else{
			chrome.storage.sync.set({"twitNicData": "n/a"});	
		}
  
  }
  
  
function neutralize(){
    var pro = $('input[name=pronoun]:checked', '#choosePls').val(); 
    console.log(pro);
    //alert(pro);
    
    //calls a different .js file for each pronoun choice
    //the evaluation is done on a page-by-page level, not directly in this file for the extension
    if (pro == "m"){ 
        console.log("m chosen");
        chrome.tabs.executeScript( { file: 'm.js'}); 
        console.log("m executed");
    } else{
        if (pro == "f"){ 
            console.log("f chosen");
            chrome.tabs.executeScript( { file: 'f.js' }); 
            console.log("f executed");
        } else{ 
            if (pro == "t") { 
                console.log("t chosen");
                chrome.tabs.executeScript( { file: 't.js' }); 
                console.log("t executed");
            }     
        }
    }
    
    
};
         