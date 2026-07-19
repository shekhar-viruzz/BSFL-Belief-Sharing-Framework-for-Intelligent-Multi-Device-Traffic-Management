import traci


class VehicleManager:

    def __init__(self):
        self.vehicles = {}

    def update(self):

        ids = traci.vehicle.getIDList()

        self.vehicles.clear()

        for vid in ids:

            lane = traci.vehicle.getLaneID(vid)

            density = len(traci.lane.getLastStepVehicleIDs(lane))

            self.vehicles[vid] = {

                "id": vid,

                "position": traci.vehicle.getPosition(vid),

                "speed": traci.vehicle.getSpeed(vid),

                "acceleration": traci.vehicle.getAcceleration(vid),

                "waiting_time": traci.vehicle.getWaitingTime(vid),

                "lane": lane,

                "road": traci.vehicle.getRoadID(vid),

                "angle": traci.vehicle.getAngle(vid),

                "type": traci.vehicle.getTypeID(vid),

                "density": density

            }

    def get_all(self):
        return self.vehicles

    def count(self):
        return len(self.vehicles)
