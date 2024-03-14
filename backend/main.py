# import generate_schedule
import genetic_algorithm
import scheduler_entities
from typing import List
from scheduler_entities import Task, Squad
import json

tasks_csv = "data/tasks.csv"
squads_csv = "data/squads.csv"
tasks = scheduler_entities.generate_tasks_from_file(tasks_csv)
squads = scheduler_entities.generate_squads_from_file(squads_csv)

# initialize a population of size n
n = 100
population = genetic_algorithm.initialize_population(n, tasks, squads)

# select pairs from the top 50% of the population    
top_pairs, individual_scores, fitness_scores = genetic_algorithm.select_pairs(population)




num_gens = 50
print("Generation 0:", fitness_scores)
max_score = max(fitness_scores)
sol = individual_scores[max_score]

for i in range(1, num_gens + 1):
    
    # mutate the offspring
    children, generation = genetic_algorithm.crossover(top_pairs, individual_scores, fitness_scores, squads)

    for child in children:
        population.append(child)
    top_pairs, individual_scores, fitness_scores = genetic_algorithm.select_pairs(population)
    new_max = max(fitness_scores)
    if new_max > max_score:
        max_score = new_max
        sol = individual_scores[max_score]


print("Final Generation:", fitness_scores)
data = {}
data["score"] = max_score
for squad in sol:
    squad_tasks = {}
    for assignment in squad.assigned_tasks:
        task = str(assignment[0])
        time = assignment[1].time()
        squad_tasks[str(time)] = task
    data[str(squad.squad_id)] = squad_tasks

filename = "solution.json"

with open(filename, 'w') as file:
    json.dump(data, file, indent=4)
