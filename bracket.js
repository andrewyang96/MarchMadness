function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return "";
}

var modifyDOM = function (data) {
	// console.log(data);
	
	// modify bracket DOM
	var bitstringIndex = 1;
	var rndnum = 2;
	data['matches'].forEach(function (rnd) {
		var matchnum = 1; // matchnum % 2 == 1 for slot 1s, matchnum % 2 == 0 for slot 2s
		rnd.forEach(function (match) {
			match.forEach(function (team) {
				var sel = "#" + matchnum + "r" + rndnum;
				// console.log("Processing " + sel);
				$(sel + " .name").html(team['name']);
				$(sel + " .seed").html(team['seed']);
				if (parseInt(data['bitstring'][bitstringIndex]) % 2 == (matchnum-1) % 2) {
					// console.log(sel + " is a winner");
					$(sel).addClass("winner");
				}
				matchnum += 1;
			});
			bitstringIndex += 1;
		});
		rndnum += 1;
	});
	var champion = data['matches'][data['matches'].length-1][0][parseInt(data['bitstring'][63])];
	$("#champion .name").html(champion['name']);
	$("#champion .seed").html(champion['seed']);
	
	// HARDCODED: SUBJECT TO CHANGE!
	$("#first-region").html("MIDWEST");
	$("#second-region").html("WEST");
	$("#third-region").html("SOUTH");
	$("#fourth-region").html("EAST");
	
	// modify debug DOM
	$(".debug #time").html("This bracket was generated on " + data['timestamp'] + " UTC");
	var score = data['score'];
	var gamesCorrect = data['gamesCorrect'];
	var gamesCorrectList = data['gamesCorrectList'];
	if (data['isNew']) {
		// $(".debug #link a").attr("href", "/cgi-bin/bracket.py?id=" + data['uniqueID']);
		$(".debug #link").html("<a href='/bracket.html?id=" + data['uniqueID'] + "'>Permalink to generated bracket</a>");
		$("#refreshmessage a").html("Your bracket would have scored " + score + " points and had " + gamesCorrect + " out of 63 games correct. (" +  gamesCorrectList + ") Refresh this page for another bracket");
	} else {
		$(".debug #link").html("<a href='/bracket.html'>Generate another bracket</a>");
		$("#refreshmessage a").html("Your bracket would have scored " + score + " points and had " + gamesCorrect + " out of 63 games correct. (" +  gamesCorrectList + ") Refresh this page for another bracket");
	}
	
	// tweet button
	$("iframe").attr("src", $("iframe").attr("src") + "%3Fid%3D" + data['uniqueID']);
};

$(document).ready(function () {
	var URL = "http://bracketodds.cs.illinois.edu/cgi-bin/api.py";
	var id = getQueryVariable("id");
	if (id) {
		URL += ("?id=" + id);
	}
	$.ajax({
		url: URL,
		dataType: "json",
		success: function (data) {
			modifyDOM(data);
		}
	});
});