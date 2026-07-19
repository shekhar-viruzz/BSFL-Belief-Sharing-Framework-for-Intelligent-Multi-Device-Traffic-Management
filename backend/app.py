from sumo.simulation import Simulation
from sumo.vehicle_manager import VehicleManager
from sumo.rsu_manager import RSUManager

from ai.belief_manager import BeliefManager
from ai.fusion_engine import FusionEngine

from communication.v2v_manager import V2VManager
from communication.v2i_manager import V2IManager

from routing.route_manager import RouteManager

from ws_server.phone_server import (
    start_server,
    send_to_device,
    get_device_results
)

import time


def main():

    print("===================================")
    print("Starting BSFL Traffic Intelligence System...")
    print("===================================")

    # Start WebSocket server
    start_server()

    # Give server time to start
    time.sleep(2)

    # Start SUMO
    simulation = Simulation()
    simulation.start()

    # Initialize modules
    vehicles = VehicleManager()

    rsu = RSUManager()
    rsu.initialize()

    belief = BeliefManager()

    v2v = V2VManager()
    v2i = V2IManager()

    fusion = FusionEngine()

    route = RouteManager()

    print("System Initialized\n")

    try:

        while True:

            # ----------------------------------
            # SUMO STEP
            # ----------------------------------

            simulation.step()

            vehicles.update()

            vehicle_data = vehicles.get_all()

            # ----------------------------------
            # SEND EVERY VEHICLE TO DEVICE
            # ----------------------------------

            for vid, vehicle in vehicle_data.items():

                packet = {

                    "type": "predict",

                    "vehicle_id": str(vid),

                    "speed": float(
                        vehicle.get("speed", 0.0)
                    ),

                    "waiting_time": float(
                        vehicle.get("waiting_time", 0.0)
                    ),

                    "density": float(
                        vehicle.get("density", 0.0)
                    ),

                    "acceleration": float(
                        vehicle.get("acceleration", 0.0)
                    )

                }

                print("Sending:", packet)

                send_to_device(packet)

            # ----------------------------------
            # RECEIVE AI RESULTS
            # ----------------------------------

            device_results = get_device_results()

            if device_results:

                print("\nAI Results:")
                print(device_results)

            belief.update_from_phone(device_results)

            belief_data = belief.all()

            # ----------------------------------
            # RSU
            # ----------------------------------

            rsu.update(vehicle_data)

            # ----------------------------------
            # V2V
            # ----------------------------------

            v2v.broadcast(
                vehicle_data,
                belief_data
            )

            # ----------------------------------
            # V2I
            # ----------------------------------

            v2i.send_to_rsu(
                vehicle_data,
                belief_data,
                rsu.get_all()
            )

            # ----------------------------------
            # FUSION
            # ----------------------------------

            fusion.fuse(
                v2i.get_reports()
            )

            fusion_state = fusion.get_all()

            # ----------------------------------
            # ROUTING
            # ----------------------------------

            route.process(
                fusion_state,
                vehicle_data
            )

            # ----------------------------------
            # STATUS
            # ----------------------------------

            print("\n===================================")

            print(
                f"Vehicles Active : {vehicles.count()}"
            )

            belief.print_summary()

            v2v.print_status()

            v2i.print_status()

            fusion.print_status()

            route.print_status()

            rsu.print_status()

            print("===================================\n")

    except KeyboardInterrupt:

        print("\nStopping BSFL System...")

    finally:

        try:
            simulation.close()
        except Exception as e:
            print("SUMO closed:", e)


if __name__ == "__main__":
    main()
