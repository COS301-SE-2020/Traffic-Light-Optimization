#!/usr/bin/env python

import os
import sys
import optparse
from django.conf import settings
import threading
import random 
import time

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

# Global variable to stop connection
STOPPER = { 'SUMO': True }


# Gobal array to contain the 
RECORDER = { 'Info': True }

# Extra info calculator
def calculate_extra_info(traci_connection, roads_in, roads_out):
    entry = {}
    co2 = 0.0
    fuel = 0.0
    cars = 0.0
    for roadId in roads_in:
        entry[roadId] = traci_connection.edge.getLastStepVehicleNumber(roadId) 
        cars += entry[roadId]
        co2 += traci_connection.edge.getCO2Emission(roadId)
        fuel += traci_connection.edge.getFuelConsumption(roadId)
    
    for roadId in roads_out:
        cars += traci_connection.edge.getLastStepVehicleNumber(roadId) 
        co2 += traci_connection.edge.getCO2Emission(roadId)
        fuel += traci_connection.edge.getFuelConsumption(roadId)
    entry["co2"] = co2
    entry["fuel"] = fuel
    entry["cars"] = cars

    return entry


# Contains TraCI control loop 
def run(traci_connection, intersection_id, loop=True, roads_in=[], roads_out=[]):
    #global STOPPER 
    STOPPER[str(intersection_id)] = False
    step = 0
    path = settings.MEDIA_ROOT + "\simulation\inter"+ str(intersection_id)
    if not os.path.isdir(path):
        os.mkdir(path)
    
    # Adjust the Simulation view and get the screenshot of the first UI view
    traci_connection.gui.setZoom( "View #0", 100 )
    traci_connection.gui.screenshot("View #0", path+"\image"+str(step)+".png", width=1000, height=800)

    # Get Extra Information for intersection 
    roads_in = [ "in" + str(road.get("position")) for road in roads_in ]
    roads_out = [ "out" + str(road.get("position")) for road in roads_out ]
    if loop:
        RECORDER[str(intersection_id)] = [ calculate_extra_info(traci_connection,roads_in,roads_out) ]
    
    step += 1

    # Iterate throughout the simulation if loop is true i.e. we want the simulation not only the visualization
    # while traci_connection.simulation.getMinExpectedNumber() > 0 and loop and not STOPPER[str(intersection_id)]:
    while traci_connection.simulation.getMinExpectedNumber() > 0 and not STOPPER[str(intersection_id)]:
        traci_connection.simulationStep()
        print(step)
        traci_connection.gui.screenshot("View #0", path+"\image"+str(step)+".png", width=1000, height=800)
        step += 1
        if not loop:
            break
        RECORDER[str(intersection_id)].append( calculate_extra_info(traci_connection,roads_in,roads_out) )

    # Close the simulation
    traci_connection.close()
    sys.stdout.flush()

# Puause the traCi Simulation
def simulation_info( intersection_id, iteration ):
    inter_info = RECORDER[str(intersection_id)]
    info = inter_info[iteration]
    return info 

# Stop the traCi simulation
def stop( connection_label, intersection_id ):
    STOPPER[str(intersection_id)] = True
    time.sleep(1)


# main entry point
def initiate( intersection_id, looper=True , simu_connection=123, roads_in=[], roads_out=[] ):
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    threadId = str(simu_connection)

    path = os.getcwd() + "\main_app\simulation\generic"
    sumocfg = os.getcwd() + "\main_app\media\config\intersection\simulation\inter_"+str(intersection_id)+".sumocfg"
    tripinfo = os.getcwd() + "\main_app\media\config\intersection\\tripinfo\inter_"+str(intersection_id)+"_"+str(threadId)+".xml"
    print(sumocfg)
    print(tripinfo)
    try:
        traci.start([sumoBinary, "-c", sumocfg , "--tripinfo-output", tripinfo, "-S", "-Q"], label=str(threadId))
        traci_connection = traci.getConnection(str(threadId))
        run(traci_connection,intersection_id, loop=looper, roads_in=roads_in, roads_out=roads_out)
    except:
        print("********************************* >> Something went wrong << ******************************* ")
        #traci_connection = traci.getConnection( str(intersection_id) )
        #traci_connection.close()
        #sys.stdout.flush()


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

