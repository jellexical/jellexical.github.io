var PUBLIC_KEY_ADDRESS       = "https://raw.githubusercontent.com/jellexical/jellexical.github.io/master/public.key";
var PUBLIC_KEY               = "";
var WEBSOCKET_SERVER_ADDRESS = "ws://127.0.0.1:9000";
var WEBSOCKET                = null;

function createWebSocket() {
    $.ajax({url: PUBLIC_KEY_ADDRESS, success: function(result) {
        PUBLIC_KEY = result;
        WEBSOCKET = new WebSocket(WEBSOCKET_SERVER_ADDRESS);
    }});
}

function encryptText(text) {
    if (PUBLIC_KEY === "") {
        return "";
    } else {
        var rsa = new JSEncrypt();
        rsa.setPublicKey(PUBLIC_KEY);
        ciphertext = rsa.encrypt(text);
        return ciphertext;
    }
}