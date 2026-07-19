class BeliefManager:


    def __init__(self):

        self.beliefs = {}

        print(
            "✅ OnePlus AI Belief Manager Loaded"
        )



    # ==================================
    # RECEIVE RESULTS FROM PHONE AI
    # ==================================

    def update_from_phone(
        self,
        phone_results
    ):

        if phone_results:

            for vid, result in phone_results.items():

                self.beliefs[vid] = {

                    "belief": result["belief"],

                    "confidence": result["confidence"]

                }



    # ==================================
    # OLD FUNCTION KEPT FOR COMPATIBILITY
    # ==================================

    def update(
        self,
        vehicles
    ):

        pass



    def get(
        self,
        vehicle_id
    ):

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



            elif b["belief"] == "CONGESTION":

                congestion += 1




        print(
            "\n====== AI BELIEFS ======"
        )


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
