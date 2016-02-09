import autobahn.asyncio
import asyncio
import py.game
import py.server
import py.server.protocol


if __name__ == "__main__":
    factory = autobahn.asyncio.WebSocketServerFactory("ws://127.0.0.1:9000", debug=True)
    factory.protocol = py.server.protocol.ServerProtocol

    loop = asyncio.get_event_loop()
    core = loop.create_server(factory, "0.0.0.0", 9000)
    server = loop.run_until_complete(core)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
