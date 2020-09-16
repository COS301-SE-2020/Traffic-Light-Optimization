#!/usr/bin/env python

import os
import sys
import optparse
from django.conf import settings

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


# Setting options for running SUMO
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run(traci_connection, intersection_id):
    step = 0
    path = settings.MEDIA_ROOT + "\simulation\inter"+ str(intersection_id)
    if not os.path.isdir(path):
        os.mkdir(path)

    traci_connection.gui.setZoom( "View #0", 100 )
    while traci_connection.simulation.getMinExpectedNumber() > 0:
        traci_connection.simulationStep()
        print(step)
        traci_connection.gui.screenshot("View #0", path+"\image"+str(step)+".png", width=1000, height=800)
        step += 1

    traci_connection.close()
    sys.stdout.flush()

# Puause the traCi Simulation
def pause():
    pass

# Stop the traCi simulation
def stop():
    traci.close() 


# main entry point
def initiate( intersection_id ):
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    path = os.getcwd() + "\main_app\simulation\generic"
    sumocfg = os.getcwd() + "\main_app\media\config\intersection\simulation\inter_"+str(intersection_id)+".sumocfg"
    tripinfo = os.getcwd() + "\main_app\media\config\intersection\\tripinfo\inter_"+str(intersection_id)+".xml"
    print(sumocfg)
    print(tripinfo)
    try:
        traci.start([sumoBinary, "-c", sumocfg , "--tripinfo-output", tripinfo], label=str(intersection_id))
        traci_connection = traci.getConnection(str(intersection_id))
        run(traci_connection,intersection_id)
    except:
        print("********************************* >> Something went wrong")
        traci_connection = traci.getConnection(str(intersection_id))
        traci_connection.close()
        #traci.start([sumoBinary, "-c", sumocfg , "--tripinfo-output", tripinfo], label=str(intersection_id))
        #traci_connection = traci.getConnection(str(intersection_id))
    
    
    #traci.start([sumoBinary, "-c", path+"\\sumo.sumocfg", "--tripinfo-output", path+"\\tripinfo.xml", "-S", "-Q"])
    #traci.start([sumoBinary, "-c", "sumo.sumocfg", "--tripinfo-output", "tripinfo.xml", "-S", "-Q"])
    #traci.start([sumoBinary, "-c", str(intersection.intersection_simulation.url), "--tripinfo-output", "tripinfo.xml", "-S", "-Q"])


if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "sumo.sumocfg", "--tripinfo-output", "tripinfo.xml", "-S", "-Q"])
    run()

