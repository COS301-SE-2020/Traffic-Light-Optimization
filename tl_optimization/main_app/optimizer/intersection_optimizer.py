import json
from pyeasyga import pyeasyga


# Time Series forecast ...............................
def forecast( data=[] ):
    pass 

# define a fitness function
def intersection_fitness(individual, data):
    intersection = []
    for road in intersection:
        wait_time = road * traffic_lights
        #accumulated_traffic = 
        #freed_cars_per_cycle = 
    return values

def fitness(individual, data):
    values, weights = 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
    if weights > 15:
        values = 0
    return values

# Genetic Algorithm ..................................
def traffic_light_optimizer( data=[], road_info =[] ):
    # Setup data: Intersection information
    road_info = [
        {"road_name": "r111" , "capacity": 45 , "rate": 0.6 , "out": "A" ,"direction": "left"} ,
        {"road_name": "r111" , "capacity": 45 , "rate": 0.2 , "out": "B" ,"direction": "right"} ,
        {"road_name": "r201" , "capacity": 45 , "rate": 0.3 , "out": "A" ,"direction": "left"} ,
        {"road_name": "r201" , "capacity": 45 , "rate": 0.7 , "out": "B" ,"direction": "right"}
    ]

    # setup data
    data = [{'name': 'box1', 'value': 4, 'weight': 12},
        {'name': 'box2', 'value': 2, 'weight': 1},
        {'name': 'box3', 'value': 10, 'weight': 4},
        {'name': 'box4', 'value': 1, 'weight': 1},
        {'name': 'box5', 'value': 2, 'weight': 2}]

    ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data
    ga.fitness_function = fitness               # set the GA's fitness function
    ga.run()                                    # run the GA
    results = ga.best_individual() 
    print( results )            # print the GA's best solution
    return results

if __name__ == '__main__':
    traffic_light_optimizer()