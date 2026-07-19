import traci

SUMO_BINARY = "sumo"
SUMO_CONFIG = "/home/darwin/BSFL/maps/noida/noida.sumocfg"

traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])

tls = traci.trafficlight.getIDList()

print(f"\nTraffic Lights Found: {len(tls)}\n")

for tl in tls:
    lanes = traci.trafficlight.getControlledLanes(tl)
    print(f"Traffic Light: {tl}")
    print(f"Controlled Lanes: {lanes}")

    if lanes:
        lane = lanes[0]
        shape = traci.lane.getShape(lane)
        print(f"Approx Position: {shape[0]}")
    print("-" * 40)

traci.close()
