import random
import numpy as np
from datetime import datetime, timedelta
# import genetic_algorithm_operations
# import scheduler_entities
from typing import List
from scheduler_entities import Task, Squad

import copy

"""
    Initializes a population of a specified size
"""
def initialize_population(size: int, tasks: List[Task], squads: List[Squad]):
    # initial variables
    tasks_size = len(tasks)
    squads_size = len(squads)
    population = []

    # loop through an amount equal to the specified population size
    for _ in range(size):
        random.shuffle(tasks)
        random.shuffle(squads)
        # create deep copies of squads and tasks lists
        squad_copy = copy.deepcopy(squads)
        task_copy = copy.deepcopy(tasks)

        for task in task_copy:
            task_assigned, squads_assigned = task.assign_squads_to_task(squad_copy)
            # check if task was successfully assigned
            if task_assigned:
                # assign squads of returned squad indexes to the task
                for index in squads_assigned:
                    squad_copy[index].assign_task(task)
            
        
        population.append(squad_copy)
        
    return population
        

def select_pairs(population):
    individual_scores = {}
    for i in range(len(population)):
        fitness_sum = 0
        individual = population[i]
        for squad in individual:
            for task, _ in squad.assigned_tasks:
                fitness_sum += task.priority
        individual_scores[fitness_sum] = individual

    fitness_scores = list(individual_scores.keys())
    # print(len(fitness_scores))
    fitness_scores.sort(reverse=True)
    fitness_scores = fitness_scores[:len(fitness_scores) // 2] # Top 50% of individuals in the population

    # calculate total fitness
    total_fitness = sum(fitness_scores)
    
    # Calculate selection probabilities
    selection_probabilities = [score / total_fitness for score in fitness_scores]
    # Select pairs of parents
    pairs = []
    population_size = len(fitness_scores)
    for _ in range(population_size):
        # Select first parent
        index1 = select_individual(selection_probabilities)
        
        # Select second parent (ensure different from first parent)
        index2 = select_individual(selection_probabilities)
        while index2 == index1:
            index2 = select_individual(selection_probabilities)
        
        pairs.append((index1, index2))
    
    return pairs, individual_scores, fitness_scores

def select_individual(selection_probabilities):
    # Perform roulette wheel selection
    random_value = random.random()
    cumulative_probability = 0
    for index, probability in enumerate(selection_probabilities):
        cumulative_probability += probability
        if random_value <= cumulative_probability:
            return index

def crossover(pairs, individual_scores, fitness_scores, squads):
    children = []
    generations = {}
    # Iterate through each pair
    for index_i, index_j in pairs:
        score_i = fitness_scores[index_i]
        score_j = fitness_scores[index_j]

        indiv_i = individual_scores[score_i]
        indiv_j = individual_scores[score_j]
        rate = 0.1
        tasks = []
        new_child = mutation(indiv_i, indiv_j, rate, tasks, squads)
        generations[(index_i, index_j)] = new_child
        children.append(new_child)

    return children, generations

def mutation(indiv_i, indiv_j, rate, origin_tasks, origin_squads):
    parent_tasks = []
    parent_ids = []
    squads = copy.deepcopy(origin_squads)
    tasks = copy.deepcopy(origin_tasks)
    for squad in indiv_i:
        for assignment in squad.assigned_tasks:
            task = assignment[0]
            id = task.task_id
            if id not in parent_ids:
                parent_tasks.append(task)
                parent_ids.append(id)
    for squad in indiv_j:
        for assignment in squad.assigned_tasks:
            task = assignment[0]
            id = task.task_id
            if id not in parent_ids:
                parent_tasks.append(task)
                parent_ids.append(id)
    
    # for squad in indiv_j:
    #     for assignment in squad.assigned_tasks:
    #         parent_tasks.add(assignment[0])
    # print(parent_tasks)
                
    """
    Handle mutation by performing a mutation check on each task. If
    the check passes, either add a new task or replace it.
    """
    for task in parent_tasks:
        x = random.random() # generate a random number [0, 1)
        if x < rate: # check if mutation occurs
            y = random.random() # new random number to choose operation
            if y < 0.5: # add new task
                for new_task in tasks:
                    id = new_task.task_id
                    if id not in parent_ids: # found a task not in the parents task list
                        parent_tasks.append(new_task)
                        parent_ids.append(id)
                        break
            else: # replace the task with a different one
                for new_task in tasks:
                    id = new_task.task_id
                    if id not in parent_ids: # found a task not in the parents task list
                        parent_tasks.append(new_task)
                        parent_ids.append(id)
                        parent_tasks.remove(task)
                        parent_ids.remove(task.task_id)
                        break

    random.shuffle(parent_tasks)
    random.shuffle(squads)

    for task in parent_tasks:
        task_assigned, squads_assigned = task.assign_squads_to_task(squads)
        if task_assigned:
            # assign squads of returned squad indexes to the task
            for index in squads_assigned:
                squads[index].assign_task(task)        
    
    return squads

        

# def genetic_algorithm(tasks, resources, num_generations=100, population_size=10, mutation_rate=0.1):
#     """
#     Implement the Genetic Algorithm for project scheduling.
    
#     Parameters:
#     - tasks: List of tasks with their durations.
#     - resources: List of available resources.
#     - num_generations: Number of generations to evolve through.
#     - population_size: Size of the population per generation.
#     - mutation_rate: Probability of mutation per gene.
    
#     Returns:
#     - best_schedule: The best schedule found across all generations.
#     - best_fitness: The fitness score of the best schedule.
#     """
#     # Initialize the population with random schedules
#     population = [genetic_algorithm_operations.generate_schedule(tasks, resources) for _ in range(population_size)]
#     best_schedule = None
#     best_fitness = float('inf')
    
#     # Main GA loop
#     for generation in range(num_generations):
#         # Calculate fitness for each individual in the population
#         fitness_scores = [genetic_algorithm_operations.calculate_fitness(schedule) for schedule in population]
        
#         # Update the best schedule found so far
#         for i, fitness in enumerate(fitness_scores):
#             if fitness < best_fitness:
#                 best_fitness = fitness
#                 best_schedule = population[i]
                
#         # Selection - select individuals to breed
#         selected_individuals = genetic_algorithm_operations.selection(population, fitness_scores)
        
#         # Crossover - create next generation's population
#         next_generation = []
#         while len(next_generation) < population_size:
#             parent1, parent2 = random.sample(selected_individuals, 2)
#             offspring1, offspring2 = genetic_algorithm_operations.crossover(parent1, parent2, crossover_rate=1.0)  # Assuming always crossover
#             next_generation.extend([offspring1, offspring2])
        
#         # Mutation
#         next_generation = [genetic_algorithm_operations.mutate_schedule(schedule, mutation_rate, tasks, resources) for schedule in next_generation]
        
#         # Prepare for the next generation
#         population = next_generation[:population_size]
        
#     return best_schedule, best_fitness

def fifo_schedule(tasks, squads):
    """
    Schedules tasks to squads using a First in, First out strategy.

    Parameters:
    - tasks: a list of task dictionaries.
    - squads: a list of squad lists with available time.

    Returns:
    - A tuple containing the schedule and its fitness value.
    """
    tasks = sorted(tasks, key=lambda x: x['arrival_time'])  # FIFO ordering, sorts tasks by arrival time 
    schedule = []
    fitness = 0
    squad_index = 0

    for task in tasks:
        squad_time = squads[squad_index][1]
        if squad_time >= task['time']:
            # Assign task to squad and update squad's available time
            schedule.append((squad_index + 1, task['id']))
            squads[squad_index][1] -= task['time']
            fitness += task['time']  # Add task time to fitness
        else:
            # If the current squad doesn't have enough time, move to the next squad
            squad_index = (squad_index + 1) % len(squads)
            if squads[squad_index][1] >= task['time']:
                schedule.append((squad_index + 1, task['id']))
                squads[squad_index][1] -= task['time']
                fitness += task['time']
            else:
                # If no squad can take the task, it's a scheduling failure
                raise ValueError("Scheduling failure: no available squad for task.")
    
    return schedule, fitness
