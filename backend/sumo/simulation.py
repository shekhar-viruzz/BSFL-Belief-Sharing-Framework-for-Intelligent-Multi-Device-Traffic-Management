import os
import traci

SUMO_BINARY = "sumo-gui"

SUMO_CONFIG = os.path.expanduser(
    "~/BSFL/maps/noida/noida.sumocfg"
)


class Simulation:

    def __init__(self):
        self.running = False

    def start(self):
        traci.start([
            SUMO_BINARY,
            "-c",
            SUMO_CONFIG
        ])
        self.running = True
        print("✅ SUMO Started")

    def step(self):
        traci.simulationStep()

    def close(self):
        traci.close()
        self.running = False
        print("Simulation Closed")
