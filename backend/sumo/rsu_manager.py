import math
import traci


class RSU:


    def __init__(self, rsu_id, x, y, radius=300):

        self.id = rsu_id

        self.x = x

        self.y = y

        self.radius = radius

        self.connected = []

        self.beliefs = []

        self.state = "NORMAL"



class RSUManager:


    def __init__(self):

        self.rsus = []



    def initialize(self):

        tls = traci.trafficlight.getIDList()


        for tl in tls:


            lanes = traci.trafficlight.getControlledLanes(tl)


            if len(lanes) == 0:

                continue



            shape = traci.lane.getShape(

                lanes[0]

            )


            x, y = shape[0]



            self.rsus.append(

                RSU(

                    tl,

                    x,

                    y,

                    300

                )

            )



        print(

            f"\nLoaded {len(self.rsus)} RSUs"

        )





    def update(self, vehicles):


        for rsu in self.rsus:


            rsu.connected.clear()



            for vehicle in vehicles.values():


                vx, vy = vehicle["position"]



                distance = math.sqrt(

                    (vx-rsu.x)**2 +

                    (vy-rsu.y)**2

                )



                if distance <= rsu.radius:


                    rsu.connected.append(

                        vehicle["id"]

                    )





    def get_all(self):


        data = {}



        for rsu in self.rsus:


            data[rsu.id] = {


                "position": (

                    rsu.x,

                    rsu.y

                ),


                "vehicles": rsu.connected,


                "state": rsu.state

            }



        return data





    def print_status(self):


        print("\n====== RSUs ======")



        for rsu in self.rsus:


            print(

                rsu.id,

                "Vehicles:",

                len(rsu.connected)

            )
