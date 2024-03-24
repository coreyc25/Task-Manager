import csv

# reads the input file and creates a list of task with each one
# represented by a dictionary.
# The key for each task is an integer, task_id
def read_file(input_file):
    data = []
    with open(input_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        task_id = 1
        for row in csv_reader:
            # initialize a single task from row in input file
            task_dict = {}
            task_dict['id'] = task_id
            task_dict['task name'] = row['Task Name']
            task_dict['priority'] = int(row['Priority'])
            task_dict['squads'] = int(row['Squads'])
            task_dict['time'] = time_to_minutes(row['Time'])

            data.append(task_dict)
            task_id += 1
    return data

# converts a string representing time (HH:MM) to an integer
# equal to the same time in minutes
def time_to_minutes(time):
    hours, minutes = map(int, time.split(':'))
    total_minutes = hours * 60 + minutes
    return total_minutes

# converts an integer representing minutes to a military time string
def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}{minutes:02d}"

# algorithm used to assign squads to each task
# returns a dictionary of assignments where each key is a squad id
# and the values are a list of task ids that were assigned to that squad
def assign_troop_to_task(squads, tasks):
    assignments = {}
    for squad in squads:
        assignments[squad[0]] = []

    for task in tasks:
        # extract values from task dictionary
        task_id = task['id']
        task_name = task['task name']
        task_squads = task['squads']
        task_time = task['time']
        
        task_assignments = []
        # iterate through list of squads
        for squad in squads:
            # extra values from squad tuple
            squad_id = squad[0]
            squad_time = squad[1]

            # if the squad has time available
            if squad_time >= task_time:

                # append the squad id to the task's assignments
                task_assignments.append(squad_id)

                # append the task id to the squad's assignments
                assignments[squad_id].append(task_id)

                # decrement the squad time and the task squads
                squad[1] -= task_time
                task_squads -= 1
            # end the loop if enough squads have been assigned
            if task_squads == 0:
                break
        
        # if the task was assigned enough squads, give the assigned squads time back
        if task_squads != 0:
            for squad_id in task_assignments:
                assignments[squad_id].remove(task_id)
                squads[squad_id - 1][1] += task_time

    return assignments

# displays the assignments in an easy to read format
def display_assignments(assignments, task_list):

    # iterate through the assignments 
    for squad_id in assignments:
        tasks = assignments[squad_id]
        task_schedule = []

        # initialize time and day for formatting purposes
        cur_time = 0
        cur_day = 1

        # iterate through the task ids for current squad
        for cur_task_id in tasks:

            # iterate through the task list, searching for the matching task for current task id
            for task in task_list:
                task_id = task['id']
                task_name = task['task name']
                task_time = task['time']

                # task id and current task id match found
                if cur_task_id == task_id:
                    
                    # format time
                    start_time = cur_time
                    end_time = task_time + cur_time
                    start_day = cur_day
                    end_day = cur_day
                    while end_time > 1440:
                        end_day += 1
                        end_time -= 1440

                    # create time string
                    time_str = 'From day ' + str(start_day) +  ', ' + minutes_to_time(start_time) + ' to day ' + str(end_day) + ', ' + minutes_to_time(end_time)
                    
                    # update current time and day to the end time and day
                    cur_time = end_time
                    cur_day = end_day

                    task_schedule.append((task_name, time_str))
                    break
        assignments[squad_id] = task_schedule
    
    return assignments

# function to generate a text file that details the squads assignments
# in a neat and easy to read format
def generate_file(assignments):
    output_file = 'troop_assignments.txt'
    with open(output_file, 'w') as file:
        for key, value in assignments.items():
            file.write(f"Squad {key}'s assignments are as follows:\n")
            for task, time_range in value:
                file.write(f"{time_range}: {task}\n")
            file.write("\n")

def main():
    # generate task_list: a list of task dictionaries
    input_file = 'tasks.csv'
    task_list = read_file(input_file)

    # sort in descending order of priority
    task_list = sorted(task_list, key=lambda x: int(x['priority']), reverse=True)

    # constraints
    days_available = 7 # CHANGE THIS TO SEE DIFFERENT OUTPUTS
    time_available = 24 * 60 * days_available
    squads_available = 2 # OR THIS TOO I GUESS

    # create squad_list, a list of lists representing a squad id and their available time
    squad_list = [[i + 1, time_available] for i in range(squads_available)]

    # call algorithm to generate task assignments
    assignments = assign_troop_to_task(squad_list, task_list)
    
    assignments = display_assignments(assignments, task_list)

    generate_file(assignments)

if __name__ == "__main__":
    main()