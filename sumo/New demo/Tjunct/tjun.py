#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(step)

        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        det_vehs1 = traci.inductionloop.getLastStepVehicleIDs("det_1")
        det_vehs2 = traci.inductionloop.getLastStepVehicleIDs("det_2")

        for veh in det_vehs:
            print(veh)
            #traci.vehicle.changeLane(veh, 2, 25)

        # if step == 100:
        #     traci.vehicle.changeTarget("1", "e9")
        #     traci.vehicle.changeTarget("3", "e9")

        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    
    traci.start([sumoBinary, "-c", "sumo.sumocfg",
                             "--tripinfo-output", "tripinfo.xml","-S", "-Q" ])
    run()


 #-Q, --quit-on-end  
#Quits the GUI when the simulation

  #-G, --game   Start the GUI in gaming mode
  #-S, --start    Start the simulation after loading

