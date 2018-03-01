let ws = new WebSocket("ws://"+ window.location.host + "/ws")


ws.onmessage = function (event) {

    let data = JSON.parse(event.data);
    if(data.type == "message") {
        let username = data.username;
        let msg = data.message;

        let content = document.getElementById("ws_message_frame_content");
        let temp = document.getElementById("ws_temp");
        temp.innerText = ": " + msg + '\n';
        let initHTML = temp.innerHTML;
        temp.innerHTML = '';
        content.innerHTML = content.innerHTML + '<a class="ws_message_frame_user" href="user/' + username + '" target="_blank">' + username + '</a>' + initHTML;

        let contentFrame = document.getElementById("ws_message_frame");
        contentFrame.scrollTop = contentFrame.scrollHeight;
    }
    else if(data.type == "user") {
        let username = data.username;
        let action = data.action;

        let content = document.getElementById("ws_message_frame_content");
        content.innerHTML = content.innerHTML +
            '<p class="ws_message_frame_action"><a href="user/' + username + '" target="_black">' + username + "</a> has " + action + " this chatroom</p>";
    }
    else if(data.type == "denied") {
        window.alert("You don't has the permission to " + data.permission);
    }
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