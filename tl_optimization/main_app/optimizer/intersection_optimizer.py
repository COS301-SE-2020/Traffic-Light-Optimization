import json
import random
from pyeasyga import pyeasyga


# Time Series forecast .................................................................................
def forecast( data=[] ):
    pass 

# define a fitness function ............................................................................
def intersection_fitness(individual, data):
    #print( individual )
    intersection = []
    road_freed_number_of_cars , road_timing, road_rate, capacity = 0, 0, 0, 0
    name = data[0].get('road_name')

    for timing , traffic_light in zip(individual, data):
        if traffic_light.get('road_name') == name: 
            acceleration = traffic_light.get("rate") * traffic_light.get("rate")
            road_freed_number_of_cars = timing * traffic_light.get("rate") + ( timing * acceleration)
            road_timing = road_timing + timing
            road_rate = road_rate + traffic_light.get("rate")
            capacity = traffic_light.get("capacity")
        else:
            intersection.append( 
                {"name": name, 
                "freed_number_of_cars": road_freed_number_of_cars, 
                "timing": road_timing, 
                "rate": road_rate, 
                "capacity": capacity  }
            )
            road_freed_number_of_cars , road_timing, road_rate, capacity = 0, 0, 0, 0
            name = traffic_light.get('road_name')
            acceleration = traffic_light.get("rate") * traffic_light.get("rate")
            road_freed_number_of_cars = timing * traffic_light.get("rate") + ( timing * acceleration)
            road_timing = road_timing + timing
            road_rate = road_rate + traffic_light.get("rate")
            capacity = traffic_light.get("capacity")

    intersection.append( 
        {"name": name, 
        "freed_number_of_cars": road_freed_number_of_cars, 
        "timing": road_timing, 
        "rate": road_rate, 
        "capacity": capacity  }
    )
    error = 0
    for road in intersection:
        wait_time = sum( [ _.get("timing") for _ in intersection ] ) - road.get("timing")
        accumulated_traffic = wait_time * road.get("rate")
        conjestion_rate = accumulated_traffic - road.get("freed_number_of_cars")
        capacity_error = accumulated_traffic - ( road.get("capacity") / 7 )
        error = error + conjestion_rate + capacity_error
    return error

def fitness(individual, data):
    values, weights = 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
    if weights > 15:
        values = 0
    return values

# Initial population ................................................................................
def create_individual(data):
    return [random.randint(1, 60) for _ in range(len(data))] 

# Initial population ................................................................................
def mutate(individual):
    mutate_index = random.randrange(len(individual))
    individual[mutate_index] = random.randint(1, 60)
   

# Genetic Algorithm .................................................................................
def traffic_light_optimizer( road_info=[] ):
    # Setup data: Intersection information
    if len(road_info) == 0:
        road_info = [
            {"road_name": "r111" , "capacity": 45 , "rate": 0.6 , "out": "A" ,"direction": "left"} ,
            {"road_name": "r111" , "capacity": 45 , "rate": 0.2 , "out": "B" ,"direction": "right"} ,
            {"road_name": "r201" , "capacity": 45 , "rate": 0.3 , "out": "A" ,"direction": "left"} ,
            {"road_name": "r201" , "capacity": 45 , "rate": 0.3 , "out": "B" ,"direction": "right"}
        ]

    # setup data
    data = [{'name': 'box1', 'value': 4, 'weight': 12},
        {'name': 'box2', 'value': 2, 'weight': 1},
        {'name': 'box3', 'value': 10, 'weight': 4},
        {'name': 'box4', 'value': 1, 'weight': 1},
        {'name': 'box5', 'value': 2, 'weight': 2}]

    ga = pyeasyga.GeneticAlgorithm(road_info,
                                population_size=50,
                                generations=100,
                                crossover_probability=0.8,
                                mutation_probability=0.02,
                                elitism=True,
                                maximise_fitness=False)        # initialise the GA with data
    ga.create_individual = create_individual
    ga.mutate_function = mutate
    ga.fitness_function = intersection_fitness                  # set the GA's fitness function
    ga.run()                                                    # run the GA
    results = ga.best_individual() 
    print( results )                                            # print the GA's best solution
    return results

if __name__ == '__main__':
    traffic_light_optimizer()