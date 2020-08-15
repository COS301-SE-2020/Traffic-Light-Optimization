import os
import  sys
import optparse

if 'SUMO_HOME' in os.environ:
     sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "/path/to/sumo-gui"
sumoCmd = [sumoBinary, "-c", "4way.sumocfg"]

import traci
traci.start(sumoCmd)
step = 0
while step < 1000:
   traci.simulationStep()
   if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
       traci.trafficlight.setRedYellowGreenState("0", "GrGr")
   step += 1

traci.close()