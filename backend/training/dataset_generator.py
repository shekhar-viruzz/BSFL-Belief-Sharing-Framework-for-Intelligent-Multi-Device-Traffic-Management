import sys
import os
import csv
import traci

# Add backend folder to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from sumo.simulation import Simulation


# Save inside backend/training/
OUTPUT_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "priority_dataset.csv"
)


class DatasetGenerator:


    def __init__(self):

        self.previous_speed = {}

        self.sample_count = 0


        self.file = open(
            OUTPUT_FILE,
            "w",
            newline=""
        )


        self.writer = csv.writer(
            self.file
        )


        self.writer.writerow(
            [
                "vehicle_id",
                "speed",
                "waiting_time",
                "density",
                "acceleration",
                "priority"
            ]
        )


        print(
            "Saving dataset:",
            OUTPUT_FILE
        )



    # Priority label generation
    def calculate_priority(
        self,
        speed,
        waiting_time,
        density,
        acceleration
    ):


        priority = 0.0



        # waiting condition
        if waiting_time > 30:

            priority += 0.5

        elif waiting_time > 10:

            priority += 0.3



        # speed condition
        if speed < 2:

            priority += 0.3

        elif speed < 8:

            priority += 0.15



        # traffic density

        if density > 60:

            priority += 0.2

        elif density > 30:

            priority += 0.1



        # sudden braking

        if acceleration < -2:

            priority += 0.1



        return min(
            priority,
            1.0
        )




    def collect(self):


        vehicles = traci.vehicle.getIDList()



        for vid in vehicles:


            try:


                speed = traci.vehicle.getSpeed(
                    vid
                )


                waiting_time = traci.vehicle.getWaitingTime(
                    vid
                )


                lane = traci.vehicle.getLaneID(
                    vid
                )


                density = len(
                    traci.lane.getLastStepVehicleIDs(
                        lane
                    )
                )



                previous_speed = self.previous_speed.get(
                    vid,
                    speed
                )


                acceleration = (
                    speed - previous_speed
                )


                self.previous_speed[vid] = speed



                priority = self.calculate_priority(

                    speed,

                    waiting_time,

                    density,

                    acceleration

                )



                self.writer.writerow(
                    [

                        vid,

                        round(speed,3),

                        round(waiting_time,3),

                        density,

                        round(acceleration,3),

                        round(priority,3)

                    ]
                )


                self.sample_count += 1



            except Exception as e:

                print(
                    "Vehicle error:",
                    vid,
                    e
                )



        # write immediately

        self.file.flush()





    def close(self):

        self.file.close()





def main():


    print(
        "================================="
    )

    print(
        " REAL SUMO DATA COLLECTION"
    )

    print(
        "================================="
    )


    simulation = Simulation()


    simulation.start()



    generator = DatasetGenerator()



    try:


        TOTAL_STEPS = 5000



        for step in range(TOTAL_STEPS):


            simulation.step()


            generator.collect()



            if step % 100 == 0:


                print(
                    "Step:",
                    step,
                    "Samples:",
                    generator.sample_count
                )



    except KeyboardInterrupt:


        print(
            "Collection stopped by user"
        )



    finally:


        generator.close()


        simulation.close()



        print(
            "================================="
        )

        print(
            "Dataset completed"
        )

        print(
            "Total samples:",
            generator.sample_count
        )

        print(
            "Saved:",
            OUTPUT_FILE
        )

        print(
            "================================="
        )




if __name__ == "__main__":

    main()
