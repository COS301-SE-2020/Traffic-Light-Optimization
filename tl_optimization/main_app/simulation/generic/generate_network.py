import re
import lxml.etree
import lxml.builder
import subprocess
#from .simulation import *



class GenerateNetwork:

    def __init__(self,type="cross-road", roads_in=[], roads_out=[], lights=[] ):
        super().__init__()
        self.type = type
        self.roads_in = roads_in
        self.roads_out = roads_out
        self.lights = lights 
    
    # Nodes (intersections/junctions): Generate the .nod.xml file ................................................................
    def intersection_nodes(self):
        E = lxml.builder.ElementMaker()
        Nodes = E.nodes
        Node = E.node

        # Create the xml tree based on the type of intersection ....
        arrayOfNodes = []
        if self.type != "tup":
            arrayOfNodes.append( Node(id="A", x="0.0", y="+500.0", type="priority") )
        if self.type != "tdown":
            arrayOfNodes.append( Node(id="C", x="0.0", y="-500.0", type="priority"), )
        if self.type != "tleft":
            arrayOfNodes.append( Node(id="D", x="-500.0", y="0.0", type="priority"), )
        if self.type != "tright":   
            arrayOfNodes.append( Node(id="B", x="+500.0", y="0.0", type="priority"), )

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
        handle1=open('intersection.nod.xml','r+')
        handle1.write( the_doc )
        handle1.close()


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
        handle1=open('roads.edg.xml','r+')
        handle1.write( the_doc )
        handle1.close()

    
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
                    
                    idVal = str(roadin.get("position")) + "_" + str(roadout.get("position"))
                    begin_t = "0"
                    end_t = "100"
                    cars_hour = str(roadin.get("rate"))
                    from_ = "in" + str(roadin.get("position"))
                    to_ = "out" + str(roadout.get("position"))
                    
                    edg = Flow(id=idVal, begin=begin_t , end=end_t, vehsPerHour=cars_hour, from_=from_, to=to_ )
                    the_doc.append( edg )


        the_doc = re.sub('xsi', 'xmlns:xsi', lxml.etree.tostring(the_doc, pretty_print=True).decode('utf-8'))
        the_doc = re.sub('noNamespaceSchemaLocation', 'xsi:noNamespaceSchemaLocation', the_doc)
        the_doc = re.sub('from_', 'from', the_doc)
        # Print the xml information ............
        print("------------------------------------------------------------------------------------------------------------")
        print( the_doc )
        print("------------------------------------------------------------------------------------------------------------")

        # Save XML information to file .........
        handle1=open('traffic.rou.xml','r+')
        handle1.write(the_doc )
        handle1.close()

    # Creates the intersection
    def create_network(self):
        self.intersection_nodes()
        self.road_edges()
        self.cars_particles()
        #initiate()
        #subprocess.Popen('python .\simulation.py',shell=True) .......................................................................
        

if __name__ == "__main__":
    
    in_data = [{'name': 'r89', 'capacity': 23, 'speed': 86, 'position': 'A', 'lanes': 1, 'rate':100},
                {'name': 'r475', 'capacity': 12, 'speed': 32, 'position': 'B', 'lanes': 1, 'rate':100},
                {'name': 'jack7865', 'capacity': 65, 'speed': 32, 'position': 'C', 'lanes': 1, 'rate':100}]

    out_data = [{'name': 'r505', 'capacity': 0, 'speed': 30, 'position': 'A', 'lanes': 1},
                {'name': 'wegeg', 'capacity': 32, 'speed': 7, 'position': 'B', 'lanes': 1},
                {'name': 'u758', 'capacity': 78, 'speed': 45, 'position': 'C', 'lanes': 1}]

    simulation = GenerateNetwork( type="tleft", roads_in=in_data, roads_out=out_data  )
    # Create Nodes 
    simulation.intersection_nodes()

    # Create Edges
    simulation.road_edges()

    # Create Vehicles
    simulation.cars_particles()

    # Create Network
    #simulation.create_network()