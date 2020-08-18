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