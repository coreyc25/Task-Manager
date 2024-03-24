import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CreateTask from './CreateTask';
import TasksTable from './TasksTable';

function TaskFormDisplay() {
  const [tasksData, setTaskData] = useState([]);

  const fetchTasks = async () => {
    try {
      const endpoint = 'http://127.0.0.1:8000/api/load-tasks-table/';
      const response = await axios.get(endpoint);
      setTaskData(response.data);
    } catch (error) {
      console.error('Error fetching MongoDB data:', error);
    }
  };
  
  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className='row mx-4'>
      <CreateTask fetchTasks={fetchTasks}/>
      <TasksTable tasksData={tasksData} fetchTasks={fetchTasks} />
    </div>
  );
}

export default TaskFormDisplay;
