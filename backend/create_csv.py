import csv
import random

def generate_time():
    # Generate a random time in "H:MM" format (9 hours or less)
    hours = random.randint(0, 9)
    minutes = random.randint(0, 59)
    return f"{hours}:{minutes:02d}"

def generate_tasks(num_tasks):
    # Generate a list of tasks
    tasks = []
    for _ in range(num_tasks):
        task_name = f"Task {_ + 1}"
        priority = random.randint(1, 100)
        squads = random.randint(1, 3)
        time = generate_time()
        tasks.append([task_name, priority, squads, time])
    return tasks

def write_tasks_to_csv(tasks, filename):
    # Write tasks to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Task Name', 'Priority', 'Squads', 'Time'])
        writer.writerows(tasks)

# Generate tasks
tasks = generate_tasks(30)

# Write tasks to CSV file
write_tasks_to_csv(tasks, 'tasks.csv')
