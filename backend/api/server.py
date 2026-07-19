from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

phone_socket = None


@app.get("/")
async def root():
    return {"status": "BSFL Backend Running"}


@app.websocket("/ws/phone")
async def phone_ws(websocket: WebSocket):
    global phone_socket

    await websocket.accept()
    phone_socket = websocket

    print("\n📱 Phone Connected")
    print("Client:", websocket.client)

    try:
        while True:
            message = await websocket.receive_text()
            print("Phone ->", message)

    except WebSocketDisconnect:
        print("📴 Phone Disconnected")
        phone_socket = None
