import math


class V2VManager:


    def __init__(self, communication_range=100):

        self.communication_range = communication_range

        self.received_beliefs = {}



    def distance(self, pos1, pos2):

        x1, y1 = pos1
        x2, y2 = pos2

        return math.sqrt(
            (x2-x1)**2 +
            (y2-y1)**2
        )



    def broadcast(self, vehicles, beliefs):


        self.received_beliefs = {}


        vehicle_ids = list(vehicles.keys())


        for sender in vehicle_ids:


            if sender not in beliefs:
                continue


            sender_position = vehicles[sender]["position"]


            message = beliefs[sender]


            for receiver in vehicle_ids:


                if sender == receiver:
                    continue


                receiver_position = vehicles[receiver]["position"]


                d = self.distance(
                    sender_position,
                    receiver_position
                )


                if d <= self.communication_range:


                    if receiver not in self.received_beliefs:

                        self.received_beliefs[receiver] = []


                    self.received_beliefs[receiver].append({

                        "from": sender,

                        "belief":
                        message["belief"],

                        "confidence":
                        message["confidence"],

                        "distance":
                        round(d,2)

                    })



    def get_vehicle_messages(self, vehicle_id):

        return self.received_beliefs.get(
            vehicle_id,
            []
        )



    def print_status(self):

        total = 0


        for messages in self.received_beliefs.values():

            total += len(messages)


        print("\n====== V2V ======")

        print(
            "Messages exchanged:",
            total
        )
