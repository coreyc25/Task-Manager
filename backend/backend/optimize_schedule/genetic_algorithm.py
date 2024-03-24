# import generate_schedule
# import genetic_algorithm
# import scheduler_entities
from backend.optimize_schedule.scheduler_entities import Task, Squad
from datetime import datetime, time
from typing import List
import json
import random
import copy

"""
Temporary function to handle processing task dependencies.
Need a more efficient method for the overall system.
"""
def handle_depends(tasks: List[Task]):
    for task in tasks:
        cur_depends = task.depends
        new_depends = []
        if len(cur_depends) == 0:
            continue
        for task_name in cur_depends:
            for match_task in tasks:
                if task_name == match_task.task_name:
                    new_depends.append(match_task)
                    break
        task.depends = new_depends

"""
Initializes a list of Task objects and a list of Squad objects

Parameters:
- task_data: a list of jsons containing information for tasks
- squad_num: an int representing the number of squads available for tasks
"""
def init_tasks_squads(task_data, squad_num):
    tasks = []
    for task_id in range(len(task_data)):
        # load information from json into a new task object
        task_json = task_data[task_id]
        task_name = task_json['task_name']
        priority = int(task_json["priority"])
        depends = [task_str.strip() for task_str in task_json['depends'].split(',')]
        squads_needed = int(task_json["squads"])
        duration = int(task_json["hours"]) * 60 + int(task_json["minutes"])
        # create new task and add to tasks list
        new_task = Task(str(task_id), task_name, depends, priority, squads_needed, duration)
        tasks.append(new_task)
    handle_depends(tasks) # TEMPORARY SOLUTION FOR HANDLING DEPENDENCIES
    
    squads = []
    for squad_id in range(squad_num):
        # set availability time to 9am - 5pm of current day
        current_day = datetime.now().date()
        start_time = time(hour=9, minute=0, second=0)
        avail_start = datetime.combine(current_day, start_time)
        end_time = time(hour=17, minute=0, second=0)
        avail_end = datetime.combine(current_day, end_time)
        # create new squad and add to squads list
        new_squad = Squad(str(squad_id), avail_start, avail_end)
        squads.append(new_squad)

    # return newly created lists for tasks and squads
    return tasks, squads

"""
Processes the dependencies of a task and returns a boolean indicating if
assignment was successful.
"""
def assign_depends(task: Task, squad_copy: List[Squad]):
    # if the task has no dependencies, simply return true
    if len(task.depends) == 0:
        return True
    for cur_task in task.depends:
        # if current task is already assigned, check next one
        if cur_task.assigned:
            continue
        # recursively check for dependencies
        if assign_depends(cur_task, squad_copy):
            task_assigned = cur_task.assign_squads_to_task(squad_copy)
            # if a dependency was NOT assigned successfully, return false
            if not task_assigned:
                return False
        # if this task's dependencies were not assigned, return false
        else:
            return False
    # if all dependencies were assigned, return true
    return True

"""
Create an assignment between tasks and squads, creating a deep copy of each
to avoid affecting the original lists. Using this method of dependency handling
likely causes bias towards tasks that are dependencies for other tasks.

Parameters:
- task: a list of Task objects to be assigned to squads
- squads: a list of Squad objects to be assigned tasks

Returns:
- a deepcopy of the original squads list that has
been assigned sets of tasks
"""
def create_assignment(tasks: List[Task], squads: List[Squad]):
    # create deepcopies of the squads and tasks
    squad_copy = copy.deepcopy(squads)
    task_copy = copy.deepcopy(tasks)

    for task in task_copy:
        task.assigned = False
        for depend in task.depends:
            depend.assigned = False
    # iterate through the tasks list and attempt to assign each task
    for task in task_copy:
        # check if task has already been assigned
        if task.assigned:
            continue
        # check if task's dependencies have been assigned
        if assign_depends(task, squad_copy):
            task.assign_squads_to_task(squad_copy)

    return squad_copy

"""
Initializes a population of a specified size

Parameters:
- n: an int representing the size of the population
"""
def init_pop(n: int, tasks: List[Task], squads: List[Squad]):

    # loop through n iterations, creating a solution to add to the population list
    population = []
    for _ in range(n):
        # randomize the order tasks and squads to generate unique solutions
        random.shuffle(tasks)
        random.shuffle(squads)
        
        assigned_squad = create_assignment(tasks, squads)

        population.append(assigned_squad)

    return population

"""
Calculates the fitness score of a given population of solutions

Parameters:
- population: the list of solutions to calculate the fitness score of

Return:
- A list of tuples in format (score, sol) where 'score' is the calculated
fitness score of a solution 'sol'.
- A dictionary where keys are a fitness score and the value is a corresponding
solution
"""
def calculate_fit(population):
    # create a list of tuples of a solution and its fitness score
    indiv_scores = []
    # create a dictionary where fitness scores are keys
    unique_scores = {}
    for indiv in population:
        # track tasks added to fitness score to avoid repeats in cases where squads have the same tasks
        task_ids = set()
        fitness_score = 0
        # iterate through all assigned tasks in solution
        for squad in indiv:
            for task, _ in squad.assigned_tasks:
                # if task has been accounted for, skip it
                cur_id = task.task_id
                if cur_id in task_ids:
                    continue
                task_ids.add(cur_id)
                # if not, increment fitness score
                fitness_score += task.priority
        indiv_scores.append((fitness_score, indiv))
        unique_scores[fitness_score] = indiv
    
    return indiv_scores, unique_scores

"""
Extract the top 50% of individuals from the population based on fitness score and use it
to create pairs of individuals (to act as parents). Pair selection is based on weighted
fitness scores.

Parameters:
- population: the list of individual solutions to create pairs from.
"""
def select_pairs(indiv_scores):
    # top 50% of individuals in the population
    top_scores = sorted(indiv_scores, key=lambda x: x[0])
    top_scores = top_scores[len(top_scores) // 2:]
    # calculate total fitness
    total_score = sum(x[0] for x in top_scores)
    # calculate selection probabilities
    select_probs = [x[0] / total_score for x in top_scores]
    #create new population of top 50% of individuals
    new_population = [x[1] for x in top_scores]
    # select n pairs of parents, where n is population size
    pairs = []
    for _ in range(len(select_probs)):
        # Select first parent
        parent1 = top_scores[select_individual(select_probs)]
        # Select second parent (ensure different from first parent)
        parent2 = top_scores[select_individual(select_probs)]
        while parent1 == parent2:
            parent2 = top_scores[select_individual(select_probs)]
        pairs.append((parent1, parent2))
    return pairs, new_population

"""
Helper function for select_pairs function to select one individual from the population
using roulette wheel selection. Returns the corresponding index from the selection probabilities.
"""
def select_individual(select_probs):
    # Perform roulette wheel selection
    random_value = random.random()
    cumulative_probability = 0
    for index, probability in enumerate(select_probs):
        cumulative_probability += probability
        if random_value <= cumulative_probability:
            return index

"""
Performs crossover and mutation for each pair of parent solutions to produce offspring solutions.
Crossover strategy involves creating a list of tasks performed by the squads of the parent
solutions and then mutate this newly created task list.

Parameters:
- pairs: a list of tuples that contains the two parents
- mutate_rate: rate of mutation to use for mutation operations

Returns:
- The offspring produced by each pair of parents
"""
def crossover(pairs, squads, tasks, rate):
    offspring = []
    # Iterate through each pair of parents
    for parent_1, parent_2 in pairs:
        # extract individual solutions from the pair of parents
        indiv_1 = parent_1[1]
        indiv_2 = parent_2[1]
        # track the tasks performed by the parents
        parent_tasks = []
        parent_ids = set()
        for indiv in [indiv_1, indiv_2]:
            for squad in indiv:
                for assignment in squad.assigned_tasks:
                    task = assignment[0]
                    id = task.task_id
                    # if the task has not already been tracked, track it
                    if id not in parent_ids:
                        parent_tasks.append(task)
                        parent_ids.add(id)
        child = mutation(squads, tasks, parent_tasks, parent_ids, rate)
        offspring.append(child)

    return offspring

"""
Handles mutation by generating a random number to compare to our mutation rate for each task. If
mutation is successful, we perform one of three operations:
- Addition: add a new task from our original tasks to our parent tasks list 
- Replacement: replace the task with a different task from our original tasks list
- Reorder: move this task to the end of our task list to change the sequence of task assignments
"""
def mutation(squads, tasks, parent_tasks, parent_ids, rate):
    for task in parent_tasks:
        x = random.random() # generate a random number [0, 1)
        if x < rate: # check if mutation occurs
            y = random.random() # new random number to choose operation
            if y < 0.3: # Addition
                for new_task in tasks:
                    id = new_task.task_id
                    if id not in parent_ids: # found a task not in the parents task list
                        parent_tasks.append(new_task)
                        parent_ids.add(id)
                        break
            elif y < 0.6: # Replacement
                for new_task in tasks:
                    id = new_task.task_id
                    if id not in parent_ids: # found a task not in the parents task list
                        parent_tasks.append(new_task)
                        parent_ids.add(id)
                        parent_tasks.remove(task)
                        parent_ids.remove(task.task_id)
                        break
            else: # Reorder
                parent_tasks.remove(task)
                parent_tasks.append(task)
    # create child assignment solution using mutated tasks list
    child = create_assignment(parent_tasks, squads)
    return child

"""
Function to put score and solution into json format
"""
def jsonify_sol(score, sol):
    assignments = {}
    for squad in sol:
        squad_tasks = {}
        for assignment in squad.assigned_tasks:
            task = str(assignment[0].task_name)
            time = assignment[1].time()
            squad_tasks[str(time)] = task
        assignments[str(int(squad.squad_id) + 1)] = squad_tasks

    solution = {}
    solution["score"] = score
    solution["assignments"] = assignments

    return solution

def generate_solution(task_data, squad_num):
    # hyperparameters
    N = 500 # population size
    G = 10 # maximum generations for the same delta value
    R = 0.4 # mutation rate

     # initialize list of Task objects and list of Squad objects
    tasks, squads = init_tasks_squads(task_data, squad_num)

    # initialize population of individual solutions
    population = init_pop(N, tasks, squads)

    # calculate the fitness scores of individual solutions of the population 
    indiv_scores, unique_scores = calculate_fit(population)

    # select pairs from the top 50% of the population    
    pairs, population = select_pairs(indiv_scores)

    # record the max score and corresponding solution
    max_score = max(x[0] for x in indiv_scores)
    sol = unique_scores[max_score]
    # iterate through generations of the algorithm until we reach convergence
    # (delta value remains unchanged through G generations, indicating a plateau)
    delta = float('inf')
    count = 0
    while delta >= 0 and count < G:
        # produce the offspring using parent pairs
        offspring = crossover(pairs, squads, tasks, R)
        # add new children to the population, we are NOT removing parents
        for child in offspring:
            population.append(child)
        # cycle of calculating individual solution scores and pairing the top 50% of the population
        indiv_scores, unique_scores = calculate_fit(population)
        pairs, population = select_pairs(indiv_scores)
        # calculate resulting new max score and delta
        new_max = max(x[0] for x in indiv_scores)
        delta = new_max - max_score
        count += 1
        # delta has changed, so reset plateau count
        if delta > 0:
            count = 0
        # replace old score and solution if new score is greater
        if new_max > max_score:
            max_score = new_max
            sol = unique_scores[max_score]

    solution = jsonify_sol(max_score, sol)

    return solution