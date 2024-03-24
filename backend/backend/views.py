from django.shortcuts import render
from django.http import JsonResponse
from backend.optimize_schedule.genetic_algorithm import generate_solution
from pymongo import MongoClient
import json
from bson import ObjectId  

MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'mydb'
TASKS_COLLECTION = 'tasks'

def load_tasks_table(request):
    # MongoDB information
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[TASKS_COLLECTION]

    # import data and close connection
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])

    client.close()

    return JsonResponse(data, safe=False)

def add_task(request):
    # MongoDB information
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[TASKS_COLLECTION]
 
    if request.method == 'POST':
        # get form data for the new task
        data = json.loads(request.body)

        task_name = data.get('task_name')
        priority = data.get('priority')
        depends = data.get('depends')
        squads = data.get('squads')
        hours = data.get('hours')
        minutes = data.get('minutes')

        # create new task json
        new_task = {
            'task_name': task_name,
            'priority': priority,
            'depends': depends,
            'squads': squads,
            'hours': hours,
            'minutes': minutes,
      }

        # add new task to tasks collection
        collection.insert_one(new_task)

        client.close()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Document added successfully'}, status=201)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def del_task(request):
    if request.method == 'POST':
        # MongoDB information
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[TASKS_COLLECTION]

        data = json.loads(request.body)

        task_id = data.get('id')
        # Delete task from MongoDB
        collection.delete_one({'_id': ObjectId(task_id)})  # Assuming task ID is stored as ObjectId

        return JsonResponse({'message': 'Task deleted successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def load_assignments(request):
    if request.method == 'POST':
        # MongoDB information
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[TASKS_COLLECTION]

        # import task data and close connection
        task_data = list(collection.find())
        client.close()

        # retrieve number of squads
        squad_num = int(request.POST.get('squads'))
        
        sol = generate_solution(task_data, squad_num)

        return JsonResponse(sol, safe=False)
    
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405) 
