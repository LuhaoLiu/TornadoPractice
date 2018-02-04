var ws = new WebSocket("ws://"+ window.location.host + "/ws")


ws.onmessage = function (event) {

    var data = JSON.parse(event.data);
    var username = data.username;
    var msg = data.message;

    var content = document.getElementById("ws_message_frame_content");
    var temp = document.getElementById("ws_temp");
    temp.innerText = ": " + msg + '\n';
    var initHTML = temp.innerHTML;
    temp.innerHTML = '';
    content.innerHTML = content.innerHTML + '<a class="ws_message_frame_user" href="user/' + username + '" target="_blank">' + username + '</a>' + initHTML;

    var contentFrame = document.getElementById("ws_message_frame");
    contentFrame.scrollTop = contentFrame.scrollHeight;
}


function send(message) {
    if (message == null || message === "" || RegExp("^[ ]+$").test(message)) {
        document.getElementById("ws_attention").innerText = "Message cannot be empty";
    }
    else if (message.length > 100) {
        document.getElementById("ws_attention").innerText = "The max length of message is 100";
    }
    else {
        document.getElementById("ws_attention").innerText = "";
        document.getElementById("ws_message_send_textbox").value = "";
        ws.send(message)
    }
}