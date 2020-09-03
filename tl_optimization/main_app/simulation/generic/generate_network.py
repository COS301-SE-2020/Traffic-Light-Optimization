
import lxml.etree
import lxml.builder
import subprocess
from .simulation import *

class GenerateNetwork:

    def __init__(self,type="cross-road", roads=[], lights=[] ):
        super().__init__()
        self.type = type 
        self.roads_in = roads
        self.lights = lights 
    
    # Nodes (intersections/junctions): Generate the .nod.xml file 
    def intersection_nodes(self):
        E = lxml.builder.ElementMaker()
        NODES = E.nodes
        NODE = E.node
        FIELD1 = E.field1
        FIELD2 = E.field2

        the_doc = NODES(
                    NODE(id="0", x="0.0", y="0.0", type="traffic_light"),
                    NODE(id="1", x="", y="", type="priority"), 
                )   

        print( lxml.etree.tostring(the_doc, pretty_print=True))
        pass

    # Edges (roads/streets): generate the .edg.xml file
    def road_edges(self):
        pass
    
    # Vehicles (trips): generate the .rou.xml file
    def cars_particles(self):
        pass

    # Creates the intersection
    def create_network(self):
        initiate()
        #subprocess.Popen('python .\simulation.py',shell=True)

