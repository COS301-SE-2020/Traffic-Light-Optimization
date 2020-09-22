# Python pip libraries required ...........
import os
import re
import lxml.etree
import lxml.builder
import subprocess
from bs4 import BeautifulSoup 
from threading import Thread
import json

# Django imports required ....................
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File




class GenerateNetwork:

    def __init__(self, intersection_obj=None , roads_in=[], roads_out=[], lights=[] ):
        super().__init__()
        self.object =  intersection_obj
        self.type = intersection_obj.intersection_type
        self.roads_in = roads_in
        self.roads_out = roads_out
        self.traffic_lights_configuration = lights 
    
    # Nodes (intersections/junctions): Generate the .nod.xml file ................................................................
    def intersection_nodes(self):
        E = lxml.builder.ElementMaker()
        Nodes = E.nodes
        Node = E.node
        # Setting the nodes position based on the length of the roads ...
        #y_nodes = [ for r in self.roads_in]
        # Create the xml tree based on the type of intersection ....
        arrayOfNodes = []
        if self.type != "T-Up":
            r = {}
            for rin in self.roads_in:
                if rin.get("position") == "A":
                    r = rin
            y_val = "+" + str(r.get("capacity"))
            arrayOfNodes.append( Node(id="A", x="0.0", y="+45", type="priority") )
        if self.type != "T-Down":
            r = {}
            for rin in self.roads_in:
                if rin.get("position") == "C":
                    r = rin
            y_val = "-" + str(r.get("capacity"))
            arrayOfNodes.append( Node(id="C", x="0.0", y="-45", type="priority"), )
        if self.type != "T-Left":
            r = {}
            for rin in self.roads_in:
                if rin.get("position") == "D":
                    r = rin
            x_val = "-" + str(r.get("capacity"))
            arrayOfNodes.append( Node(id="D", x="-45", y="0.0", type="priority"), )
        if self.type != "T-Right":   
            r = {}
            for rin in self.roads_in:
                if rin.get("position") == "B":
                    r = rin
            x_val = "+" + str(r.get("capacity"))
            arrayOfNodes.append( Node(id="B", x="+45", y="0.0", type="priority"), )

        the_doc = Nodes( Node(id="0", x="0.0", y="0.0", type="traffic_light"), 
                            xsi="http://www.w3.org/2001/XMLSchema-instance" ,
                            noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd"
                        )
        for n in arrayOfNodes:
            the_doc.append( n )

        the_doc = re.sub('xsi', 'xmlns:xsi', lxml.etree.tostring(the_doc, pretty_print=True).decode('utf-8'))
        the_doc = re.sub('noNamespaceSchemaLocation', 'xsi:noNamespaceSchemaLocation', the_doc)
        the_doc = re.sub('from_', 'from', the_doc)
        # Print the xml information ............
        print("------------------------------------------------------------------------------------------------------------")
        print( the_doc )
        print("------------------------------------------------------------------------------------------------------------")

        # Save XML information to file ......
        path = os.getcwd() + '\main_app\simulation\generic'
        file = path + '\intersection.nod.xml'
        #file = 'intersection.nod.xml'
        handle1=open(file,'r+')
        handle1.truncate(0)
        handle1.write( the_doc )
        handle1.close()

        # Write to the file on db
        filename = "inter_"+ str(self.object.id) + ".nod.xml"
        self.object.intersection_nodes.delete()
        self.object.intersection_nodes.save( filename , ContentFile( the_doc ) )


    # Edges (roads/streets): generate the .edg.xml file .............................................................................
    def road_edges(self):
        E = lxml.builder.ElementMaker()
        Edges = E.edges
        Edge = E.edge
        Neigh = E.neigh


        # Create the xml tree based on the roads information ....
        the_doc = Edges( xsi="http://www.w3.org/2001/XMLSchema-instance" ,
                            noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd" )
        
        count = 0 
        roads_out_looper = self.roads_out[:]
        for road in self.roads_in:
            idVal = "in" + str(road.get("position"))
            from_ = str(road.get("position"))
            n_lanes = str(road.get("lanes"))
            speed = str(road.get("speed"))
            len = str(road.get("capacity"))


            r_out = False

            for neighbor in roads_out_looper:
                if neighbor.get("position") == road.get("position"):
                    r_out = True
                    idVal2 = "out" + str(neighbor.get("position"))
                    to_2 = str(neighbor.get("position"))
                    n_lanes2 = str(neighbor.get("lanes"))
                    speed2 = str(neighbor.get("speed"))
                    len2 = str(neighbor.get("capacity"))

                    lane_ = idVal2 + "_" + str(neighbor.get("lanes")-1)
                    edg = Edge( Neigh( lane=lane_ ),
                                id=idVal, from_=from_, to="0", priority="1", numLanes=n_lanes , speed=speed, length=len )
                    lane_ = idVal + "_" + str(road.get("lanes")-1)
                    edg2 = Edge( Neigh( lane=lane_ ), 
                                id=idVal2, from_="0", to=to_2, priority="1", numLanes=n_lanes2 , speed=speed2, length=len2 )
                    the_doc.append( edg )
                    the_doc.append( edg2 )
                    roads_out_looper.remove(neighbor)
                    break

                    
            if not r_out:
                edg = Edge(id=idVal, from_=from_, to="0", priority="1", numLanes=n_lanes , speed=speed, length=len )
                the_doc.append( edg )
        

        for road in roads_out_looper:
            idVal = "out" + str(neighbor.get("position"))
            to_ = str(road.get("position"))
            n_lanes = str(road.get("lanes"))
            speed = str(road.get("speed"))
            len = str(road.get("capacity"))
            edg = Edge(id=idVal, from_="0", to=to_, priority="1", numLanes=n_lanes , speed=speed, length=len )
            the_doc.append( edg )

        
        the_doc = re.sub('xsi', 'xmlns:xsi', lxml.etree.tostring(the_doc, pretty_print=True).decode('utf-8'))
        the_doc = re.sub('noNamespaceSchemaLocation', 'xsi:noNamespaceSchemaLocation', the_doc)
        the_doc = re.sub('from_', 'from', the_doc)
        # Print the xml information ............
        print("------------------------------------------------------------------------------------------------------------")
        print( the_doc )
        print("------------------------------------------------------------------------------------------------------------")

        # Save XML information to file ......
        path = os.getcwd() + '\main_app\simulation\generic'
        file = path + '\\roads.edg.xml'
        #file = 'roads.edg.xml'
        handle1=open(file,'r+')
        handle1.truncate(0)
        handle1.write( the_doc )
        handle1.close()

        # Write to the file on db
        filename = "inter_"+ str(self.object.id) + ".edg.xml"
        self.object.road_edges.delete()
        self.object.road_edges.save( filename , ContentFile( the_doc ) )

    
    # Vehicles (trips): generate the .rou.xml file ...................................................................................
    def cars_particles(self):
        E = lxml.builder.ElementMaker()
        Routes = E.routes
        Flow = E.flow

        the_doc = Routes( xsi="http://www.w3.org/2001/XMLSchema-instance" ,
                            noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd"  )
        for roadin in self.roads_in:
            for roadout in self.roads_out:
                if roadout.get("position") != roadin.get("position"):
                    RATE = roadin.get("rate") / ( int(roadin.get("rate")/60)+1)
                    for i in range(int(roadin.get("rate")/60) + 1):

                        idVal = str(roadin.get("position")) + "_" + str(roadout.get("position")) + "_"+ str(i)
                        begin_t = "0"
                        end_t = "150"
                        #cars_hour = str(roadin.get("rate"))
                        cars_hour = str( RATE / (60*(len(self.roads_out)-1)))
                        from_ = "in" + str(roadin.get("position"))
                        to_ = "out" + str(roadout.get("position"))
                        
                        #edg = Flow(id=idVal, begin=begin_t , end=end_t, vehsPerHour=cars_hour, from_=from_, to=to_ )
                        edg = Flow(id=idVal, begin=begin_t , end=end_t, probability=cars_hour, from_=from_, to=to_ )
                        the_doc.append( edg )


        the_doc = re.sub('xsi', 'xmlns:xsi', lxml.etree.tostring(the_doc, pretty_print=True).decode('utf-8'))
        the_doc = re.sub('noNamespaceSchemaLocation', 'xsi:noNamespaceSchemaLocation', the_doc)
        the_doc = re.sub('from_', 'from', the_doc)
        # Print the xml information ............
        print("------------------------------------------------------------------------------------------------------------")
        print( the_doc )
        print("------------------------------------------------------------------------------------------------------------")

        # Save XML information to file .........
        path = os.getcwd() + '\main_app\simulation\generic'
        file = path + '\\traffic.rou.xml'
        #file = 'traffic.rou.xml'
        handle1=open(file,'r+')
        handle1.truncate(0)
        handle1.write(the_doc )
        handle1.close()

        # Write to the file on db
        filename = "inter_"+ str(self.object.id) + ".rou.xml"
        self.object.vehicle_routes.delete()
        self.object.vehicle_routes.save( filename , ContentFile( the_doc ) )

    # Creates the intersection
    def create_network(self):
        self.intersection_nodes()
        self.road_edges()
        self.cars_particles()

        
        # Delete all previous images before adding new once to directory
        #p = os.getcwd() +'\\images\\'              # for individual testing
        p = settings.MEDIA_ROOT + "\\simulation\\"
        for f in os.listdir(p):
            #print(f)
            if f.endswith('.png'):
                f = p+f
                os.remove(f)

        # Relative path for subprocess ( calling terminal in python)
        path = os.getcwd() + '\main_app\simulation\generic'
        path = os.getcwd() + '\main_app\media\config\intersection'
        nodes = path + '\intersection.nod.xml'
        nodes = '"'+path + '\\nodes\inter_'+ str(self.object.id) + '.nod.xml'+'"'
        #nodes = self.object.intersection_nodes.url
        edges = path + '\\roads.edg.xml'
        edges = '"'+path + '\\edges\inter_'+ str(self.object.id) + '.edg.xml'+'"'
        #edges = self.object.road_edges.url
        output = '"'+ os.getcwd() + '\main_app\simulation\generic\\road_intersection.net.xml'+'"'
        print( nodes )
        netcon = 'netconvert --node-files='+nodes+' --edge-files='+edges+' --output-file='+output
        #netcon = 'netconvert --node-files=intersection.nod.xml --edge-files=roads.edg.xml --opposites.guess.fix-lengths --output-file=road_intersection.net.xml'
        subprocess.run(netcon,shell=True)

        # Write to the file on db
        output = os.getcwd() + '\main_app\simulation\generic\\road_intersection.net.xml'
        the_doc = open(output)
        filename = "inter_"+ str(self.object.id) + ".net.xml"
        self.object.intersection_network.delete()
        self.object.intersection_network.save( filename , File( the_doc ) )
        the_doc.close()
        
        # Start simulation process
        with open(output, 'r') as f: 
            data = f.read() 
        Bs_data = BeautifulSoup(data, "xml")
        phases = Bs_data.find_all('phase')
        #traffic_lights_configuration = [ { "duration": phase.get('duration'), "state": str(phase.get('state')) } for phase in phases]
        phase = phases[0]
        state = phase.get('state')
        off = len(state) % len(self.roads_in) 
        
        highest, side = 0, ""
        if off:
            for road in self.roads_in:
                if road.get('lanes') > highest:
                    side = road.get('position')
                    highest = road.get('lanes')

        traffic_lights_configuration = []
        iter = int(len(state) / len(self.roads_in))
        for phase in phases:
            start, end = 0 , iter
            state = str(phase.get('state'))
            temp = { "duration": phase.get('duration'), "state": str(phase.get('state')) }
            for road in self.roads_in:
                if road.get('position') == side:
                    end += 1
                temp[road.get('position')] = state[start:end]
                start = end
                end += iter
            traffic_lights_configuration.append(temp)
        self.traffic_lights_configuration = traffic_lights_configuration
        self.object.traffic_light_phases = json.dumps(traffic_lights_configuration)
        self.object.save()
        #print(self.traffic_lights_configuration)
        #Thread(target=initiate).start()

    def create_simulation_configurations(self):

        # Generating the .net.xml file for simulation
        self.create_network()

        # Creating configuration file for intersection simulation 
        E = lxml.builder.ElementMaker()
        Config = E.configuration
        Input = E.input
        Net = E.netfile
        Rout = E.routefiles

        path = os.getcwd() + '\main_app\media\config\intersection'
        network = path + '\\network\inter_'+ str(self.object.id) + '.net.xml'
        edges = path + '\\routes\inter_'+ str(self.object.id) + '.rou.xml'

        the_doc = Config( 
            Input(
                Net( value=network ),
                Rout( value=edges ),
            )
         )

        the_doc = re.sub('routefiles', 'route-files', lxml.etree.tostring(the_doc, pretty_print=True).decode('utf-8'))
        the_doc = re.sub('netfile', 'net-file', the_doc)

        # Print the xml information ............
        print("------------------------------------------------------------------------------------------------------------")
        print( the_doc )
        print("------------------------------------------------------------------------------------------------------------")

        # Write to the file on db
        filename = "inter_"+ str(self.object.id) + ".sumocfg"
        self.object.intersection_simulation.delete()
        self.object.intersection_simulation.save( filename , ContentFile( the_doc ) )
         

if __name__ == "__main__":
    
    in_data = [{'name': 'r89', 'capacity': 23, 'speed': 86, 'position': 'A', 'lanes': 1, 'rate':100},
                {'name': 'r475', 'capacity': 12, 'speed': 32, 'position': 'B', 'lanes': 1, 'rate':100},
                {'name': 'jack7865', 'capacity': 65, 'speed': 32, 'position': 'C', 'lanes': 1, 'rate':100}]

    out_data = [{'name': 'r505', 'capacity': 24, 'speed': 30, 'position': 'A', 'lanes': 1},
                {'name': 'wegeg', 'capacity': 32, 'speed': 7, 'position': 'B', 'lanes': 1},
                {'name': 'u758', 'capacity': 78, 'speed': 45, 'position': 'C', 'lanes': 1}]

    simulation = GenerateNetwork( type="tleft", roads_in=in_data, roads_out=out_data  )
    # Create Nodes 
    #simulation.intersection_nodes()

    # Create Edges
    #simulation.road_edges()

    # Create Vehicles
    #simulation.cars_particles()

    # Create Network
    simulation.create_network()