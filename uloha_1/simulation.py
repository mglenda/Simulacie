from evenlib import Routine,Action,Queue,randint
import pandas as pd
import matplotlib.pyplot as plt

class Parameters():
    PEOPLE_IN_HALL_1 = 0
    PEOPLE_IN_HALL_2 = 0
    PEOPLE_ARRIVAL_MIN = 1
    PEOPLE_ARRIVAL_MAX = 9
    ELEVATOR_DEFAULT_CAPACITY = 5
    DATA: list[dict] = []
    SIMULATION_ID: int = 1

def people_arrival():
    amount = randint(Parameters.PEOPLE_ARRIVAL_MIN,Parameters.PEOPLE_ARRIVAL_MAX)
    Parameters.PEOPLE_IN_HALL_1 += amount
    #Logovanie Dat
    data_line:dict = {"simulation_id": Parameters.SIMULATION_ID
                      ,"event": "people_arrival"
                      , "location": "hall_1"
                      , "amount": amount
                      , "people_in_hall_1": Parameters.PEOPLE_IN_HALL_1
                      , "people_in_hall_2": Parameters.PEOPLE_IN_HALL_2
                      } 
    Parameters.DATA.append(data_line)

def elevator_departure(elevator_id: int,elevator_capacity: int):
    transported_people: int = 0
    if elevator_id in (1,2):
        transported_people = elevator_capacity if Parameters.PEOPLE_IN_HALL_1 > elevator_capacity else Parameters.PEOPLE_IN_HALL_1
        Parameters.PEOPLE_IN_HALL_1 -= transported_people
    else:
        transported_people = elevator_capacity if Parameters.PEOPLE_IN_HALL_2 > elevator_capacity else Parameters.PEOPLE_IN_HALL_2
        Parameters.PEOPLE_IN_HALL_2 -= transported_people
    #Logovanie Dat
    data_line = {"simulation_id": Parameters.SIMULATION_ID
                    ,"event": "departure" if transported_people > 0 else "empty_hall"
                    , "location": f"elevator_{elevator_id}"
                    , "amount": transported_people
                    , "people_in_hall_1": Parameters.PEOPLE_IN_HALL_1
                    , "people_in_hall_2": Parameters.PEOPLE_IN_HALL_2
                    }
    Parameters.DATA.append(data_line)

    if elevator_id in (1,2) and transported_people > 0:
        Parameters.PEOPLE_IN_HALL_2 += transported_people
        #Logovanie Dat
        data_line:dict = {"simulation_id": Parameters.SIMULATION_ID
                      ,"event": "people_arrival"
                      , "location": "hall_2"
                      , "amount": transported_people
                      , "people_in_hall_1": Parameters.PEOPLE_IN_HALL_1
                      , "people_in_hall_2": Parameters.PEOPLE_IN_HALL_2
                      } 
        Parameters.DATA.append(data_line)

# Nastavenie pre scenar s jednym vytahom:
# a_elevator_1_departure = Action(order_min=1,order_max=5,current_order=1)
# a_elevator_1_departure.add_routine(Routine(func=elevator_departure,elevator_id= 1,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY))

# a_people_arrival = Action(order_min=1,order_max=5,current_order=1)
# a_people_arrival.add_routine(Routine(people_arrival))

# SIMULATION_QUEUE = Queue(actions=[a_people_arrival,a_elevator_1_departure])

# Nastavenie pre scenar s dvoma vytahmi:
# a_people_arrival = Action(order_min=1,order_max=5,current_order=1)
# a_people_arrival.add_routine(Routine(people_arrival))

# a_elevator_1_departure = Action(order_min=1,order_max=5,current_order=1)
# a_elevator_1_departure.add_routine(Routine(func=elevator_departure,elevator_id= 1,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY))

# a_elevator_2_departure = Action(order_min=1,order_max=5,current_order=1)
# a_elevator_2_departure.add_routine(Routine(func=elevator_departure,elevator_id= 2,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY))

# SIMULATION_QUEUE = Queue(actions=[a_people_arrival,a_elevator_1_departure,a_elevator_2_departure])


# Nastavenie pre scenar 3 vytahy, 2 haly
a_people_arrival = Action(order_min=1,order_max=16,current_order=1)
a_people_arrival.add_routine(Routine(people_arrival))

a_elevator_1_departure = Action(order_min=1,order_max=2,current_order=1)
a_elevator_1_departure.add_routine(Routine(func=elevator_departure,elevator_id= 1,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY))

a_elevator_2_departure = Action(order_min=1,order_max=2,current_order=1)
a_elevator_2_departure.add_routine(Routine(func=elevator_departure,elevator_id= 2,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY))

a_elevator_3_departure = Action(order_min=1,order_max=2,current_order=1)
a_elevator_3_departure.add_routine(Routine(func=elevator_departure,elevator_id= 3,elevator_capacity=Parameters.ELEVATOR_DEFAULT_CAPACITY*2))

SIMULATION_QUEUE = Queue(actions=[a_people_arrival,a_elevator_1_departure,a_elevator_2_departure,a_elevator_3_departure])



MAX_STEPS_PER_SIMULATION = 200
AMOUNT_OF_SIMULATIONS = 20
CUR_STEP_COUNT = MAX_STEPS_PER_SIMULATION

while(AMOUNT_OF_SIMULATIONS > 0):
    while(CUR_STEP_COUNT > 0):
        SIMULATION_QUEUE.run_next()
        CUR_STEP_COUNT -= 1
    SIMULATION_QUEUE.reset()
    Parameters.PEOPLE_IN_HALL_1 = 0
    Parameters.PEOPLE_IN_HALL_2 = 0
    Parameters.SIMULATION_ID += 1
    CUR_STEP_COUNT = MAX_STEPS_PER_SIMULATION
    AMOUNT_OF_SIMULATIONS -= 1

df = pd.DataFrame(Parameters.DATA)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

for sim_id, group in df.groupby('simulation_id'):
    group = group.reset_index()
    plt.plot(group.index, group['people_in_hall_1'], label=f'Hall 1 - Sim {sim_id}')

plt.title('Occupancy over Time - Hall 1')
plt.xlabel('Step')
plt.ylabel('People')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Push legend outside
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

for sim_id, group in df.groupby('simulation_id'):
    group = group.reset_index()
    plt.plot(group.index, group['people_in_hall_2'], label=f'Hall 2 - Sim {sim_id}')

plt.title('Occupancy over Time - Hall 2')
plt.xlabel('Step')
plt.ylabel('People')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Push legend outside
plt.tight_layout()
plt.show()
# Save to Excel
df.to_excel("elevator_log.xlsx", index=False)
