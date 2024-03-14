import random
import numpy as np
import genetic_algorithm

def tournament_selection(population, fitnesses, tournament_size=3):
    """
    Perform tournament selection on the population.

    :param population: The current population of solutions.
    :param fitnesses: A list of fitness values corresponding to each individual in the population.
    :param tournament_size: The number of individuals participating in each tournament.
    :return: A list of individuals selected for the next generation.
    """
    selected_for_next_gen = []

    while len(selected_for_next_gen) < len(population):
        # Randomly select tournament participants
        tournament_participants = random.sample(list(enumerate(fitnesses)), tournament_size)
        
        # Determine the winner of the tournament
        winner_idx = max(tournament_participants, key=lambda participant: participant[1])[0]
        
        # Add the winner to the list of selected individuals
        selected_for_next_gen.append(population[winner_idx])

    return selected_for_next_gen

def calculate_fitness(individual, tasks, squad_list):
    """
    Calculate the fitness of an individual solution based on task priorities and squad time constraints.

    :param individual: A list representing an individual solution, where each element is the squad assigned to a task.
    :param tasks: A list of dictionaries, each representing a task with 'id', 'priority', 'squads', 'time' keys.
    :param squad_list: A list of lists, each representing a squad and its total available time.
    :return: The fitness score of the individual.
    """
    fitness = 0
    squad_time_remaining = {squad[0]: squad[1] for squad in squad_list}  # Initialize squad time remaining

    for task_index, squad_assigned in enumerate(individual):
        task = tasks[task_index]
        task_time = task['time']
        task_priority = task['priority']
        
        # Check if the assigned squad has enough time remaining to complete the task
        if squad_time_remaining[squad_assigned] >= task_time:
            fitness += task_priority  # Increase fitness by the task's priority
            squad_time_remaining[squad_assigned] -= task_time  # Deduct the task time from the squad's remaining time

    return fitness

def blend_crossover(parent1_times, parent2_times, alpha=0.5):
    """
    Perform blend crossover for the time values of two parents.

    Parameters:
    - parent1_times: array of time values for parent 1
    - parent2_times: array of time values for parent 2
    - alpha: blend factor, controls the range of the generated values

    Returns:
    - child_times: array of time values for the child
    """
    # Calculate the range between parent values
    gamma = (1. + 2. * alpha) * np.random.rand(len(parent1_times)) - alpha
    child_times = (1. - gamma) * parent1_times + gamma * parent2_times
    return child_times

def uniform_crossover(parent1_modes, parent2_modes):
    """
    Perform uniform crossover for the execution modes of two parents.

    Parameters:
    - parent1_modes: array of execution modes for parent 1
    - parent2_modes: array of execution modes for parent 2

    Returns:
    - child_modes: array of execution modes for the child
    """
    # Randomly select modes from parents
    indices = np.random.rand(len(parent1_modes)) < 0.5
    child_modes = np.where(indices, parent1_modes, parent2_modes)
    return child_modes

# Example parent time values and execution modes
parent1_times = np.array([1, 2, 3, 4, 5])
parent2_times = np.array([5, 4, 3, 2, 1])
parent1_modes = np.array([0, 1, 0, 1, 0])
parent2_modes = np.array([1, 0, 1, 0, 1])

# Perform blend crossover for time values
child_times = blend_crossover(parent1_times, parent2_times)

# Perform uniform crossover for execution modes
child_modes = uniform_crossover(parent1_modes, parent2_modes)

child_times, child_modes

def mutate_time(individual, max_time_shift, tasks, time_constraints):
    """
    Mutates the starting time of a random task in the individual's schedule.

    Parameters:
    - individual: The schedule to be mutated, represented as a dictionary where keys are task IDs and values are start times.
    - max_time_shift: The maximum amount by which a task's start time can be shifted (in either direction).
    - tasks: A list of task IDs that can be mutated.
    - time_constraints: A dictionary mapping task IDs to their time constraints (e.g., earliest start time, latest end time).

    The function selects a random task from the schedule and shifts its start time by a random amount within the allowed
    range, ensuring the new start time adheres to the task's time constraints.
    """

    # Select a random task to mutate
    task_to_mutate = random.choice(tasks)
    current_start_time = individual[task_to_mutate]

    # Determine the allowed shift range while considering the task's time constraints
    min_shift = max(time_constraints[task_to_mutate]['earliest'] - current_start_time, -max_time_shift)
    max_shift = min(time_constraints[task_to_mutate]['latest'] - current_start_time, max_time_shift)

    # Perform the mutation: shift the task's start time within the allowed range
    if max_shift > min_shift:  # Ensure there is a possible shift
        time_shift = random.randint(min_shift, max_shift)
        individual[task_to_mutate] += time_shift
    else:
        # If no shift is possible, leave the task's start time as is (could log or handle differently)
        pass

    return individual

# Example usage:
individual_schedule = {'Task1': 10, 'Task2': 20, 'Task3': 30}  # Example schedule
max_time_shift = 5  # Maximum shift of 5 units in either direction
tasks = ['Task1', 'Task2', 'Task3']  # List of tasks that can be mutated
time_constraints = {  # Example time constraints for each task
    'Task1': {'earliest': 5, 'latest': 15},
    'Task2': {'earliest': 15, 'latest': 25},
    'Task3': {'earliest': 25, 'latest': 35}
}

# Mutate the schedule
mutated_schedule = mutate_time(individual_schedule, max_time_shift, tasks, time_constraints)
mutated_schedule


def mutate_resource(individual_schedule, resource_constraints, mutation_rate=0.1):
    """
    Mutates the assigned resource for a task in the individual's schedule with a given probability.
    The mutation is constrained by the available resources for each task.

    Parameters:
    - individual_schedule: A dictionary representing the schedule of tasks with their current resources.
    - resource_constraints: A dictionary mapping each task to a list of possible resources.
    - mutation_rate: The probability of mutating the resource for each task.

    Returns:
    - The mutated individual schedule.
    """

    # Iterate through each task in the individual's schedule
    for task, current_resource in individual_schedule.items():
        # Check if mutation should occur based on the mutation rate
        if random.random() < mutation_rate:
            # Get the list of possible resources for the task, excluding the current one
            possible_resources = [r for r in resource_constraints[task] if r != current_resource]
            # If there are alternative resources available, choose one at random
            if possible_resources:
                # Mutate the resource by assigning a new one
                new_resource = random.choice(possible_resources)
                individual_schedule[task] = new_resource

    return individual_schedule

# Running the function without print statements for efficiency
mutated_schedule = mutate_resource(individual_schedule, genetic_algorithm.resource_constraints, mutation_rate=0.3)
mutated_schedule