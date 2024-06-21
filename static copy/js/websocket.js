let wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
let url = `${wsProtocol}://${window.location.host}/ws/socket-server/`
const markSocket = new WebSocket(url)
markSocket.onopen = function(e){
    markSocket.send(JSON.stringify({
        'message':'CONNECTED'
    }))
}
markSocket.onclose = function(event) {
    console.error("WebSocket closed:", event);
};