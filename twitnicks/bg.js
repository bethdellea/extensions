//chrome.tabs.executeScript({ file: 'jquery-2.1.3.js'}); 
document.getElementById('addFields').addEventListener('click', addFields);
document.getElementById('TNsubmit').addEventListener('click', saveAssoc);
//document.getElementById('remRow').addEventListener('click', remFields(this));

$(document).ready(function(){
	popFields();
    jQuery(document).on('keydown', 'input.nickField', function(ev) {
        if(ev.keyCode == 13){
            console.log("enter processed");
            $('#TNsubmit').click();
        }
    });
});

 function addFields(twithandle = '', nick = ''){
	if(typeof twithandle != 'string'){
		twithandle = '';
	}
	var fieldHTML = "<div class='row'>";
	fieldHTML += "<span class='pre'>@</span><input type='text' name='handle' class='handleField' value='"+twithandle+"' placeholder='username'>&emsp;&emsp;&mdash;&gt;&emsp;&emsp;";
	fieldHTML += "<input type='text' name='nick' placeholder='nickname' value='"+nick+"' class='nickField'> &emsp;&emsp;";
	fieldHTML += "<span class='but remRow' id='remRow' onclick='remFields(this);'>x</span> </div> <!-- row -->";
	$("#formFields").append(fieldHTML);
 
 }
 
 function remFields(fieldX){
		$(fieldX).parent().remove();
 }
  
 function popFields(){
	var nickPairs = JSON.parse(localStorage.getItem("twitNicData"));
	//var nicks = {};
	if(!$.isEmptyObject(nickPairs)){
		$.each(nickPairs, function(username, nickname){
			//nicks[username] = nickname;
			addFields(username, nickname);
		});
	}
 
 
 }
  
  
  function saveAssoc(){
	//save username + nickname pairs in local storage, nick.js will pull from local storage to set up dict of needed pairs, etc etc
    hideConfirm();
	var nickPairs = {};
	$(".row").each(function(){
		//TODO: clean input at least a little before you store -- probably simplest to just restrict it to twitter-accepted username charas and 
					//numbers + letters for username and nickname, respectively for v1
		var uname = $(this).find("input[name='handle']").val();
		var nickname = $(this).find("input[name='nick']").val();
		if(uname.length && nickname.length){
			nickPairs[uname] = nickname;
		}
	});
	if(!$.isEmptyObject(nickPairs)){//nickPairs.length){
		localStorage.setItem("twitNicData", JSON.stringify(nickPairs));  //firefox version
		//if we have entered data, save it!!
		chrome.storage.sync.set({"twitNicData": JSON.stringify(nickPairs)});
        showConfirm();
		//console.log("twitNicData:: " + nickPairs);
	} else{
			//chrome.storage.sync.set({"twitNicData": "n/a"});	
			//console.log("twitNicData: n/a");
		}
  
  }
  
  //other TODO: give option (somewhere) to save and load to .txt/.csv/whatever files for folks with lots who don't want to re-enter on cleared data
  //still later TODO: on export, allow user to select which ones get saved/exported (import should add saved assoc, not overwrite entire list)
  
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

function showConfirm(){
    $(".confirm").fadeIn("slow", function(){
        $(this).fadeOut("slow");
    });
}
       
function hideConfirm(){
    $(".confirm").fadeOut("slow");
}

