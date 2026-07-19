import asyncio
import websockets
import json
import threading


arduino_connection = None
arduino_results = {}


async def handler(websocket):

    global arduino_connection

    arduino_connection = websocket

    print("🤖 Arduino Uno Q Connected")


    try:

        async for message in websocket:

            print("Arduino:", message)

            data = json.loads(message)


            if data.get("type") == "priority_result":

                arduino_results[
                    data["vehicle_id"]
                ] = data


    except Exception as e:

        print("Arduino disconnected", e)


async def send_message(data):

    if arduino_connection:

        await arduino_connection.send(
            json.dumps(data)
        )


def send_to_arduino(data):

    if arduino_connection:

        asyncio.run_coroutine_threadsafe(
            send_message(data),
            loop
        )


def get_arduino_results():

    return arduino_results



async def server():

    global loop

    loop = asyncio.get_running_loop()

    print("Starting Arduino server 9000")


    async with websockets.serve(
        handler,
        "0.0.0.0",
        9000
    ):

        await asyncio.Future()



def start_arduino_server():

    thread = threading.Thread(
        target=lambda:
        asyncio.run(server()),
        daemon=True
    )

    thread.start()
