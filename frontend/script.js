var xhr = null;
const playerList = document.getElementById('player-list');
const counterValue = document.getElementById('turn-value');

const bestQB = document.getElementById('best-available-qb');
const nextBestQB = document.getElementById('next-best-available-qb');
const diffQB = document.getElementById('qb-diff');

const bestWR = document.getElementById('best-available-wr');
const nextBestWR = document.getElementById('next-best-available-wr');
const diffWR = document.getElementById('wr-diff');

const bestRB = document.getElementById('best-available-rb');
const nextBestRB = document.getElementById('next-best-available-rb');
const diffRB = document.getElementById('rb-diff');

const bestTE = document.getElementById('best-available-te');
const nextBestTE = document.getElementById('next-best-available-te');
const diffTE = document.getElementById('te-diff');

getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};

function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Player data received!");
        dataDiv = document.getElementById('result-container');
        // Set current data text
        const players = JSON.parse(xhr.responseText);
        players.forEach(player => {
            addPlayer(JSON.parse(player));
      });
    };
}

function getPlayers() {
    console.log("Get players...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:5000/players", true);
    // Send the request over the network
    xhr.send(null);
}

function addPlayer(player) {
    const playerItem = document.createElement('li');
    const playerText = document.createElement('span');
    const playerPosition = document.createElement('span');
    playerText.textContent = player['PLAYER NAME'];
    playerItem.tagName = player['PLAYER NAME'];
    playerItem.appendChild(playerText);
    playerPosition.textContent = player['POS'];
    playerPosition.tagName = player['POS'];
    playerItem.appendChild(playerPosition);
    const draftButton = document.createElement('button');
    draftButton.textContent = 'Drafted';
    playerItem.appendChild(draftButton);
    playerList.appendChild(playerItem);
    draftButton.addEventListener('click', function() {
        playerList.removeChild(playerItem);
        draftPlayer(player['PLAYER NAME']);
    });
}


function sendDataCallback(data) {
    console.log("Player Drafted response received!");
    const responseText = data;
    counterValue.innerHTML = responseText.turn + 1;
    console.log(responseText)
    getRecommendation();
}


function sendResetCallback() {
    // Check reset response
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Draft reset response recieved!")
    }
}


function clicked() {
    if (confirm('Do you want to submit?')) {
        reset_draft();
    } else {
        return false;
    }
 }

function reset_draft() {
    console.log("Print Here")
    if (confirm('Do you want to submit?')) {
        xhr = getXmlHttpRequestObject();
        xhr.onreadystatechange = sendResetCallback
        xhr.open("DELETE", "http://localhost:5000/players", true);
        xhr.send(null);
    }
}

// function draftPlayer(player) {
//     console.log(`Drafted ${player}`);
//     xhr = getXmlHttpRequestObject();
//     xhr.onreadystatechange = sendDataCallback;
//     // asynchronous requests
//     xhr.open("POST", "http://localhost:5000/players", true);
//     xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//     // Send the request over the network
//     xhr.send(JSON.stringify({"player":player}));
    
// }

function draftPlayer(player) {
    console.log(`Drafted ${player}`);
    $.ajax({
        url:"http://localhost:5000/players",
        type: "POST",
        headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json' 
        },
        data: JSON.stringify({"player":player}),
        dataType: 'json',
        success: sendDataCallback,
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

function sendRecommendationCallback(recommendation_data) {
    // Check response is ready or not
    console.log("Player Drafted response received!");
    const responseText = recommendation_data;
    console.log(responseText)
    bestQB.innerHTML = responseText.QB.curr_best_name + "<br> HPPR POINTS: " + responseText.QB.curr_best_hppr.toFixed(2);
    nextBestQB.innerHTML = responseText.QB.next_best_name + "<br> HPPR POINTS: " + responseText.QB.next_best_hppr.toFixed(2);
    diffQB.innerHTML = responseText.QB.diff.toFixed(2)

    bestWR.innerHTML = responseText.WR.curr_best_name + "<br> HPPR POINTS: " + responseText.WR.curr_best_hppr.toFixed(2);
    nextBestWR.innerHTML = responseText.WR.next_best_name + "<br> HPPR POINTS: " + responseText.WR.next_best_hppr.toFixed(2);
    diffWR.innerHTML = responseText.WR.diff.toFixed(2)

    bestRB.innerHTML = responseText.RB.curr_best_name + "<br> HPPR POINTS: " + responseText.RB.curr_best_hppr.toFixed(2);
    nextBestRB.innerHTML = responseText.RB.next_best_name + "<br> HPPR POINTS: " + responseText.RB.next_best_hppr.toFixed(2);
    diffRB.innerHTML = responseText.RB.diff.toFixed(2)

    bestTE.innerHTML = responseText.TE.curr_best_name + "<br> HPPR POINTS: " + responseText.TE.curr_best_hppr.toFixed(2);
    nextBestTE.innerHTML = responseText.TE.next_best_name + "<br> HPPR POINTS: " + responseText.TE.next_best_hppr.toFixed(2);
    diffTE.innerHTML = responseText.TE.diff.toFixed(2)
}


function getRecommendation() {
    console.log(`Requesting Recommendation`);
    $.ajax({
        url:"http://localhost:5000/recommendation",
        type: "GET",
        success: sendRecommendationCallback,
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}

function seachPlayers() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('player-search');
    filter = input.value.toUpperCase();
    ul = document.getElementById("player-list");
    li = ul.getElementsByTagName('li');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].children[0];
      txtValue = a.textContent;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

(function () {
    getPlayers()
    getRecommendation()
})();