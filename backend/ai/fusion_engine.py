class FusionEngine:


    def __init__(self):

        self.rsu_states = {}



    def fuse(self, rsu_reports):


        self.rsu_states = {}



        for rsu_id, reports in rsu_reports.items():


            normal_score = 0
            slow_score = 0
            congestion_score = 0


            congestion_count = 0
            slow_count = 0



            for report in reports:


                belief = report["belief"]

                confidence = report["confidence"]



                if belief == "NORMAL":

                    normal_score += confidence



                elif belief == "SLOW_TRAFFIC":

                    slow_score += confidence

                    slow_count += 1



                elif belief == "CONGESTION":

                    congestion_score += confidence

                    congestion_count += 1




            total = (

                normal_score +

                slow_score +

                congestion_score

            )



            scores = {


                "NORMAL": normal_score,

                "SLOW_TRAFFIC": slow_score,

                "CONGESTION": congestion_score

            }



            state = max(

                scores,

                key=scores.get

            )



            confidence = 0


            if total > 0:

                confidence = scores[state] / total



            # ===============================
            # CONGESTION DECISION LOGIC
            # ===============================


            vehicle_count = len(reports)


            congestion_ratio = 0

            slow_ratio = 0



            if vehicle_count > 0:


                congestion_ratio = (

                    congestion_count /

                    vehicle_count

                )


                slow_ratio = (

                    slow_count /

                    vehicle_count

                )



            # Force RSU state change

            if congestion_ratio >= 0.08:


                state = "CONGESTION"


                confidence = congestion_ratio



            elif slow_ratio >= 0.25:


                state = "SLOW_TRAFFIC"


                confidence = slow_ratio




            self.rsu_states[rsu_id] = {


                "state": state,


                "confidence": round(

                    confidence,

                    2

                ),


                "vehicles": vehicle_count,


                "congestion": congestion_count,


                "slow": slow_count

            }





    def get_all(self):

        return self.rsu_states





    def print_status(self):


        print("\n====== RSU FUSION ======")



        for rsu, data in self.rsu_states.items():


            print(

                rsu,

                "→",

                data["state"],

                "Confidence:",

                data["confidence"],

                "Vehicles:",

                data["vehicles"],

                "Congestion:",

                data["congestion"],

                "Slow:",

                data["slow"]

            )
