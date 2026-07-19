import os
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib


class BeliefManager:


    def __init__(self):

        self.beliefs = {}

        self.previous_speed = {}


        model_path = os.path.expanduser(
            "~/BSFL/backend/training/traffic_model.tflite"
        )


        scaler_path = os.path.expanduser(
            "~/BSFL/backend/training/scaler.pkl"
        )


        self.interpreter = tf.lite.Interpreter(
            model_path=model_path
        )


        self.interpreter.allocate_tensors()


        self.input_details = (
            self.interpreter.get_input_details()
        )


        self.output_details = (
            self.interpreter.get_output_details()
        )


        self.scaler = joblib.load(
            scaler_path
        )


        self.classes = [

            "CONGESTION",

            "NORMAL",

            "SLOW_TRAFFIC"

        ]


        print("✅ AI Belief Model Loaded")



    def calculate_density(self, vehicles, current_vehicle):


        density = 0


        lane = current_vehicle.get(
            "lane",
            None
        )


        for v in vehicles.values():

            if v.get("lane", None) == lane:

                density += 1


        return density




    def calculate_acceleration(self, vehicle_id, speed):


        previous = self.previous_speed.get(

            vehicle_id,

            speed

        )


        acceleration = speed - previous


        self.previous_speed[vehicle_id] = speed


        return acceleration




    def predict(
        self,
        speed,
        waiting_time,
        density,
        acceleration
    ):


        features = pd.DataFrame(

            [[

                speed,

                waiting_time,

                density,

                acceleration

            ]],

            columns=[

                "speed",

                "waiting_time",

                "density",

                "acceleration"

            ]

        )


        scaled = self.scaler.transform(

            features

        ).astype(np.float32)



        self.interpreter.set_tensor(

            self.input_details[0]["index"],

            scaled

        )


        self.interpreter.invoke()



        output = self.interpreter.get_tensor(

            self.output_details[0]["index"]

        )


        index = np.argmax(

            output[0]

        )


        confidence = float(

            output[0][index]

        )


        return {


            "belief":

            self.classes[index],



            "confidence":

            round(

                confidence,

                3

            )

        }




    def update(self, vehicles):


        for vid, vehicle in vehicles.items():


            speed = vehicle.get(

                "speed",

                0

            )


            waiting = vehicle.get(

                "waiting_time",

                0

            )


            density = self.calculate_density(

                vehicles,

                vehicle

            )



            acceleration = self.calculate_acceleration(

                vid,

                speed

            )



            result = self.predict(

                speed,

                waiting,

                density,

                acceleration

            )


            self.beliefs[vid] = result




    def get(self, vehicle_id):

        return self.beliefs.get(

            vehicle_id

        )




    def all(self):

        return self.beliefs




    def print_summary(self):


        normal = 0

        slow = 0

        congestion = 0



        for b in self.beliefs.values():


            if b["belief"] == "NORMAL":

                normal += 1



            elif b["belief"] == "SLOW_TRAFFIC":

                slow += 1



            else:

                congestion += 1




        print("\n====== AI BELIEFS ======")

        print(

            "NORMAL:",

            normal

        )

        print(

            "SLOW:",

            slow

        )

        print(

            "CONGESTION:",

            congestion

        )
