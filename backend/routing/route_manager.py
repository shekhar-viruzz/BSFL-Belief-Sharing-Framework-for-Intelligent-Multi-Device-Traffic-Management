import traci


class RouteManager:


    def __init__(self):

        # Store rerouted vehicles
        self.rerouted = set()

        # Store last reroute simulation time
        self.last_reroute = {}

        # Minimum gap between reroutes
        self.cooldown = 60



    def reroute_vehicle(self, vehicle_id):

        try:

            print("Trying reroute:", vehicle_id)



            # Check vehicle exists
            if vehicle_id not in traci.vehicle.getIDList():

                return



            current_time = traci.simulation.getTime()



            # Prevent repeated rerouting
            if vehicle_id in self.last_reroute:


                if (
                    current_time - self.last_reroute[vehicle_id]
                    < self.cooldown
                ):

                    return




            # Get current route

            current_route = traci.vehicle.getRoute(

                vehicle_id

            )


            if len(current_route) < 2:

                return



            # SUMO automatic rerouting

            traci.vehicle.rerouteTraveltime(

                vehicle_id

            )



            # Save statistics

            self.rerouted.add(

                vehicle_id

            )


            self.last_reroute[vehicle_id] = current_time



            print(

                "✅ Rerouted:",

                vehicle_id

            )



        except Exception as e:


            print(

                "Route error",

                vehicle_id,

                e

            )





    def process(self, fusion_state, vehicles):


        for rsu_id, data in fusion_state.items():



            # Only act on congestion

            if data["state"] == "CONGESTION":



                # Confidence filter

                if data["confidence"] < 0.3:

                    continue




                print(

                    "\n🚨 Congestion detected at RSU:",

                    rsu_id

                )



                count = 0



                # Reroute limited vehicles

                for vehicle_id in vehicles.keys():



                    if count >= 10:

                        break



                    self.reroute_vehicle(

                        vehicle_id

                    )


                    count += 1





    def print_status(self):


        print("\n====== ROUTING ======")


        print(

            "Vehicles rerouted:",

            len(self.rerouted)

        )
