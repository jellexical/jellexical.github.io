import autobahn.asyncio
import json
import py.server.responders


class ServerProtocol(autobahn.asyncio.WebSocketServerProtocol):

    REQUEST_TYPE        = "requestType"
    REQUEST_PAYLOAD     = "requestPayload"
    REQUEST_TYPE_LOGIN  = "login"
    REQUEST_TYPE_LOGOUT = "logout"

    def __init__(self):
        autobahn.asyncio.WebSocketServerProtocol.__init__(self)
        self.request = None
        self.identity = ""

    def onConnect(self, request):
        self.request = request

    def onMessage(self, payload, binary):
        try:
            payloadJSON = json.loads(payload.decode('utf-8'), encoding='utf-8')
            if ServerProtocol.REQUEST_TYPE not in payloadJSON or ServerProtocol.REQUEST_PAYLOAD not in payloadJSON:
                self.dropConnection()
                return
            else:
                responder = py.server.responders.getResponder(payloadJSON[ServerProtocol.REQUEST_TYPE])
                if responder is None:
                    self.dropConnection()
                    return
                else:
                    response = yield from responder.getResponse(payloadJSON[ServerProtocol.REQUEST_TYPE])
                    if response is None:
                        return
                    else:
                        if payloadJSON[ServerProtocol.REQUEST_TYPE] == ServerProtocol.REQUEST_TYPE_LOGIN:
                            if response[ServerProtocol.REQUEST_PAYLOAD]["success"] == "true":
                                self.identity = response[ServerProtocol.REQUEST_PAYLOAD]
                        elif payloadJSON[ServerProtocol.REQUEST_TYPE] == ServerProtocol.REQUEST_TYPE_LOGOUT:
                            self.identity = ""
                        self.sendMessage(json.dumps(response).encode("utf-8"))
        except json.JSONDecodeError:
            self.dropConnection()
            return
        except UnicodeError:
            self.dropConnection()
            return

