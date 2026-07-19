import requests


PHONE_IP = "192.168.1.100"   # CHANGE THIS TO YOUR ONEPLUS IP
PHONE_PORT = 8000


def predict_on_phone(
        speed,
        waiting_time,
        density,
        acceleration
):

    payload = {

        "speed": speed,
        "waiting_time": waiting_time,
        "density": density,
        "acceleration": acceleration

    }


    try:

        response = requests.post(

            f"http://{PHONE_IP}:{PHONE_PORT}/predict",

            json=payload,

            timeout=1

        )


        return response.json()


    except Exception as e:


        print(
            "Phone AI connection failed:",
            e
        )


        return {

            "belief": "NORMAL",
            "confidence": 0.0

        }
