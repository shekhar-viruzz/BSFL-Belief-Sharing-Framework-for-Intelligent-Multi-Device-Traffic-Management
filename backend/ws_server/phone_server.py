import asyncio
import json
import threading
import websockets

connected_device = None
device_results = {}
event_loop = None


# ======================================
# DEVICE CONNECTION
# ======================================

async def handler(websocket):

    global connected_device
    global event_loop

    connected_device = websocket
    event_loop = asyncio.get_running_loop()

    print("\n===================================")
    print("BSFL Device Connected")
    print("===================================")

    try:

        async for message in websocket:

            print("Received:", message)

            try:
                data = json.loads(message)

            except json.JSONDecodeError:
                print("Invalid JSON")
                continue

            msg_type = data.get("type")

            if msg_type == "belief":

                device_results[data["vehicle_id"]] = {
                    "belief": data["belief"],
                    "confidence": data["confidence"]
                }

                print(
                    "AI RESULT:",
                    data["vehicle_id"],
                    data["belief"],
                    data["confidence"]
                )

            else:
                print("Unknown message:", msg_type)

    except websockets.exceptions.ConnectionClosed:
        print("Device disconnected")

    except Exception as e:
        print("WebSocket Error:", e)

    finally:

        connected_device = None
        print("Connection closed")


# ======================================
# SEND TO DEVICE
# ======================================

async def send_message(data):

    if connected_device:

        await connected_device.send(
            json.dumps(data)
        )


def send_to_device(data):

    if connected_device and event_loop:

        asyncio.run_coroutine_threadsafe(
            send_message(data),
            event_loop
        )


# Backward compatibility
send_to_phone = send_to_device


# ======================================
# RESULTS
# ======================================

def get_device_results():
    return device_results


# Backward compatibility
get_phone_results = get_device_results


# ======================================
# SERVER
# ======================================

async def server():

    print("Starting BSFL WebSocket Server...")

    async with websockets.serve(
        handler,
        "0.0.0.0",
        8765
    ):

        print("Waiting for Device on port 8765...")

        await asyncio.Future()


# ======================================
# START SERVER
# ======================================

def start_server():

    def run():
        asyncio.run(server())

    threading.Thread(
        target=run,
        daemon=True
    ).start()


if __name__ == "__main__":
    asyncio.run(server())
