from datetime import datetime, timedelta
import csv
from typing import List
import copy

class Squad:
    def __init__(self, squad_id, available_start, available_end):
        """
        Initializes a new squad with specific attributes.
        
        Parameters:
        - squad_id (str): A unique identifier for the squad.
        - available_start (str): The start of the squad's availability window (format: 'YYYY-MM-DD HH:MM').
        - available_end (str): The end of the squad's availability window (format: 'YYYY-MM-DD HH:MM').
        - execution_modes (list): A list of execution modes the squad can perform (e.g., ['remote', 'onsite']).
        """
        self.squad_id = squad_id
        self.available_start = datetime.strptime(available_start, '%Y-%m-%d %H:%M')
        self.available_end = datetime.strptime(available_end, '%Y-%m-%d %H:%M')
        self.available_time = int((self.available_end - self.available_start).total_seconds() / 60)
        # self.execution_modes = execution_modes
        self.assigned_tasks = []  # List to hold tasks assigned to this squad.

    def assign_task(self, task):
        """
        Attempts to assign a task to the squad, considering the task's preferred execution mode and the squad's capabilities.
        
        Parameters:
        - task (Task): The task to be assigned.
        - start_time (datetime): The proposed start time for the task.
        
        Returns:
        - (bool): True if the task was successfully assigned, False otherwise.
        """
        # Check if the task's preferred execution mode matches the squad's capabilities
        # if task.preferred_execution_mode in self.execution_modes:
        task_end = self.available_start + timedelta(minutes=task.duration) # Calculate time allocated to task
        # task_end = self.available_start + time_allocated # Calculate the time the squad would finish with task
        if task_end <= self.available_end: # Check if the squad has time available for the task
            self.assigned_tasks.append((task, self.available_start))  # Assign the task
            # Update the squad's availability to reflect the task assignment
            self.available_start = task_end
            return True
        return False  # Task not assigned

    def __str__(self):
        return f"Squad {self.squad_id}"
    
    def print_schedule(self):
        for task in self.assigned_tasks:  
            print(task[0], task[1])

# Define the Task class
class Task:
    def __init__(self, task_id, task_name, task_details, priority, squads_needed, duration):
        """
        Initializes a new task with specific attributes.
        
        Parameters:
        - task_id (str): A unique identifier for the task.
        - task_name (str): Name for the actual task.
        - task_details (str): A detaield explanation of the task.
        - priority (int): A value (1-100) that gives the priority score of the task.
        - squads (int): The number of squads needed to perform the task.
        - duration (int): The duration of the task in minutes.
        - time_window_start (str): The start of the time window when the task can begin (format: 'YYYY-MM-DD HH:MM').
        - time_window_end (str): The end of the time window by which the task must be completed (format: 'YYYY-MM-DD HH:MM').
        - preferred_execution_mode (str): The preferred mode of execution for the task (e.g., 'remote', 'onsite').
        """
        self.task_id = task_id
        self.task_name = task_name
        self.task_details = task_details
        self.priority = priority
        self.squads_needed = squads_needed
        self.duration = duration
        # self.time_window_start = datetime.strptime(time_window_start, '%Y-%m-%d %H:%M')
        # self.time_window_end = datetime.strptime(time_window_end, '%Y-%m-%d %H:%M')
        # self.preferred_execution_mode = preferred_execution_mode
        self.assigned = False  # Initially, no task is assigned.
    
    """
    Assigns squads to this task, returning true if successful and false if not.
    A possible improvement would be to randomly assign the squads rather than
    doing it sequentially to create more varying outcomes.

    Parameters:
    - squads (List[Squad]): A  list of squads available to perform tasks
    """
    def assign_squads_to_task(self, squads: List[Squad]):
        squads_needed = self.squads_needed
        squads_available = len(squads)
        squad_copy = copy.deepcopy(squads)

        squads_assigned = []    
        i = 0 # squad index
        while squads_needed > 0 and i < squads_available:
            cur_squad = squad_copy[i]

            # check if the current squad is able to perform the task
            if cur_squad.assign_task(self):
                squads_needed -= 1
                squads_assigned.append(i)
            i += 1
        
        # return true if task was fully assigned along with assigned squads
        assigned = squads_needed == 0
        if assigned == 0:
            self.assigned = True
            
        return assigned, squads_assigned


    def __str__(self):
        return f"Task {self.task_id}: {self.task_name}"        


    
class Scheduler:
    def __init__(self, tasks, squads):
        """
        Initializes the scheduler with a set of tasks and squads.
        
        Parameters:
        - tasks (list): A list of Task instances to be scheduled.
        - squads (list): A list of Squad instances available for task assignments.
        """
        self.tasks = tasks
        self.squads = squads

    def assign_tasks(self):
        """
        Assigns tasks to squads based on availability, time windows, and execution modes.
        """
        for task in self.tasks:  # Iterate through each task
            for squad in self.squads:  # Iterate through each squad
                if not task.assigned:  # Proceed if the task is not already assigned
                    # Check if squad is available within the task's time window
                    # if squad.available_start >= task.time_window_start and squad.available_end <= task.time_window_end:
                        # start_time = max(squad.available_start, task.time_window_start)  # Determine the start time
                    start_time = squad.available_start
                    if squad.assign_task(task):  # Try to assign the task
                        break  # Break the loop if the task is successfully assigned




# reads the input file and creates a list of Task Objects
def generate_tasks_from_file(input_file):
    tasks = []

    # converts a string representing time (HH:MM) to an integer
    # equal to the same time in minutes
    def time_to_minutes(time):
        hours, minutes = map(int, time.split(':'))
        total_minutes = hours * 60 + minutes
        return total_minutes
    
    with open(input_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        task_id = 1
        for row in csv_reader:
            # initialize a single task from row in input file
            task_name = row['Task Name']
            priority = int(row['Priority'])
            squads = int(row['Squads'])
            duration = time_to_minutes(row['Time'])

            # the following parameters are not yet accounted for
            task_details = "N/A"
            # time_window_start = "2023-02-26 09:00"
            # time_window_end = "2023-03-03 09:00"
            # preferred_execution_mode = "remote"

            new_task = Task(task_id, task_name, task_details, priority, squads, duration)
            tasks.append(new_task) # add newly created task to tasks list
            
            task_id += 1
    return tasks

def generate_squads_from_file(input_file):
    squads = []
    
    with open(input_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # initialize a single task from row in input file
            squad_id = row['Squad ID']

            # the following parameters are not yet accounted for
            available_start = "2023-02-26 09:00"
            available_end = "2023-02-26 17:00"
            # execution_modes = ["remote", "onside"]

            new_squad = Squad(squad_id, available_start, available_end)
            squads.append(new_squad) # add newly created squad to tassquadks list
            
    return squads