class V2IManager:


    def __init__(self):

        self.rsu_reports = {}



    def send_to_rsu(self, vehicles, beliefs, rsus):


        self.rsu_reports = {}



        for vehicle_id, vehicle in vehicles.items():


            if vehicle_id not in beliefs:

                continue



            vehicle_position = vehicle["position"]



            nearest_rsu = None

            min_distance = float("inf")



            for rsu_id, rsu in rsus.items():


                rsu_position = rsu["position"]



                distance = (

                    (vehicle_position[0] - rsu_position[0]) ** 2

                    +

                    (vehicle_position[1] - rsu_position[1]) ** 2

                ) ** 0.5



                if distance < min_distance:


                    min_distance = distance

                    nearest_rsu = rsu_id




            if nearest_rsu:


                if nearest_rsu not in self.rsu_reports:

                    self.rsu_reports[nearest_rsu] = []



                self.rsu_reports[nearest_rsu].append(


                    {


                        "vehicle_id": vehicle_id,


                        "belief":

                        beliefs[vehicle_id]["belief"],



                        "confidence":

                        beliefs[vehicle_id]["confidence"],



                        "distance":

                        round(min_distance, 2)

                    }


                )



    def get_reports(self):

        return self.rsu_reports




    def print_status(self):


        total = 0



        for reports in self.rsu_reports.values():

            total += len(reports)



        print("\n====== V2I ======")



        print(

            "Reports sent to RSUs:",

            total

        )
