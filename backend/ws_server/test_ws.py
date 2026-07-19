import websocket

ws = websocket.create_connection(
    "ws://10.252.78.172:8765"
)

print("CONNECTED")

ws.close()
