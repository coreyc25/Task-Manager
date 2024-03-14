import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import CreateTask from './CreateTask';
import SquadTaskAssignments from './SquadTaskAssignments';
import TasksOverview from './TasksOverview';

function App() {
  const [activeTab, setActiveTab] = useState('createTask');
  const [tasks, setTasks] = useState([]);

  const handleAddTask = (newTask) => {
    setTasks(prevTasks => [...prevTasks, newTask]);
  };

  return (
    <div className="container mt-3">
      <ul className="nav nav-tabs">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'createTask' ? 'active' : ''}`}
            onClick={() => setActiveTab('createTask')}
          >
            Create Task
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'squadTasks' ? 'active' : ''}`}
            onClick={() => setActiveTab('squadTasks')}
          >
            Squad Task Assignments
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'tasksOverview' ? 'active' : ''}`}
            onClick={() => setActiveTab('tasksOverview')}
          >
            Tasks Overview
          </button>
        </li>
      </ul>
      <div className="tab-content mt-3">
        {activeTab === 'createTask' && <CreateTask onTaskCreate={handleAddTask} />}
        {activeTab === 'squadTasks' && <SquadTaskAssignments tasks={tasks} />}
        {activeTab === 'tasksOverview' && <TasksOverview />}
      </div>
    </div>
  );
}

export default App;
