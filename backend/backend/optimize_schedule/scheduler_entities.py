from datetime import datetime, timedelta
import csv
from typing import List
import copy

class Squad:
    def __init__(self, squad_id, avail_start, avail_end):
        """
        Initializes a new squad with specific attributes.
        
        Parameters:
        - squad_id (str): A unique identifier for the squad.
        - avail_start (datetime): The start of the squad's availability window.
        - avail_end (datetime): The end of the squad's availability window.
        """
        self.squad_id = squad_id
        self.avail_start = avail_start
        self.avail_end = avail_end
        self.avail_time = int((self.avail_end - self.avail_start)
                              .total_seconds() / 60) # total minutes available to perform tasks
        self.assigned_tasks = [] # list of assigned tasks

    def assign_task(self, task):
        """
        Attempts to assign a task to the squad
        
        Parameters:
        - task (Task): The task to be assigned.
        
        Returns:
        - (bool): True if the task was successfully assigned, False otherwise.
        """
         # calculate time allocated to task
        task_end = self.avail_start + timedelta(minutes=task.duration)
         # check if the squad has time available for the task
        if task_end <= self.avail_end:
            # assign the task and the time the task is started
            self.assigned_tasks.append((task, self.avail_start))
            # update the squad's availability 
            self.avail_start = task_end
            return True
        # not enough available time, task is NOT assigned
        return False

    def __str__(self):
        return f"Squad {self.squad_id}"
    
    # basic function to print tasks for debugging purposes
    def print_schedule(self):
        for task in self.assigned_tasks:  
            print(task[0], task[1])

# Define the Task class
class Task:
    def __init__(self, task_id, task_name, depends, priority, squads_needed, duration):
        """
        Initializes a new task with specific attributes.
        
        Parameters:
        - task_id (str): A unique identifier for the task.
        - task_name (str): Name for the actual task.
        - depends (list of Task): Task dependencies that must be completed before this task.
        - priority (int): A value (1-100) that gives the priority score of the task.
        - squads (int): The number of squads needed to perform the task.
        - duration (int): The duration of the task in minutes.
        - time_window_start (str): The start of the time window when the task can begin (format: 'YYYY-MM-DD HH:MM').
        - time_window_end (str): The end of the time window by which the task must be completed (format: 'YYYY-MM-DD HH:MM').
        - preferred_execution_mode (str): The preferred mode of execution for the task (e.g., 'remote', 'onsite').
        """
        self.task_id = task_id
        self.task_name = task_name
        self.depends = depends
        self.priority = priority
        self.squads_needed = squads_needed
        self.duration = duration
        self.assigned = False  # Initially, no task is assigned.
    
    """
    Attempt to assign required amount of  squads to this task, returning true if successful and false if not.

    Parameters:
    - squads (List[Squad]): A  list of squads available to perform tasks

    Returns:
    - assigned: a boolean indicating if the task was successfully assigned or not
    """
    def assign_squads_to_task(self, squads: List[Squad]):

        # if there are not enough squads available to complete the task, return false immediately
        squads_needed = self.squads_needed
        squads_available = len(squads)
        if squads_needed > squads_available:
            return False
        
        # iterate through a deepcopy of squads
        squad_copy = copy.deepcopy(squads)
        assigned_squads = []
        for squad in squad_copy:
            if squad.assign_task(self):
                assigned_squads.append(squad)
                squads_needed -= 1
            # if required number of squads has been assigned to this task, end function and return true
            if squads_needed == 0:
                # mark this task as assigned
                self.assigned = True
                # assign this task to the same squads in the original squads list
                for squad_new in assigned_squads:
                    for squad_orig in squads:
                        if squad_new.squad_id == squad_orig.squad_id:
                            squad_orig.assign_task(self)
                return True
        
        # if squad copy has been iterated through, task was not assigned, thus return false
        return False


    def __str__(self):
        return f"{self.task_id}: {self.task_name}"        