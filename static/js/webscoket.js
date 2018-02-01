var ws = new WebSocket("ws://"+ window.location.host + "/ws")


ws.onmessage = function (event) {

    var data = JSON.parse(event.data);
    var username = data.username;
    var msg = data.message;

    var content = document.getElementById("content");
    var temp = document.getElementById("temp");
    temp.innerText = ": " + msg + '\n';
    var initHTML = temp.innerHTML;
    temp.innerHTML = '';
    content.innerHTML = content.innerHTML + '<a href="user/' + username + '" target="_blank">' + username + '</a>' + initHTML;

    var contentFrame = document.getElementById("content_frame");
    contentFrame.scrollTop = contentFrame.scrollHeight;
}


function send(message) {
    if (message == null || message === "" || RegExp("^[ ]+$").test(message)){
        document.getElementById("attention").innerText = "Message cannot be empty.";
    }
    else if (message.length > 100){
        document.getElementById("attention").innerText = "The max length of message is 100.";
    }
    else{
        ws.send(message)
        document.getElementById("attention").innerText = "";
        document.getElementById("message").value = "";
    }
}