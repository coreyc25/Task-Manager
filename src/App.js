import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './bootstrap/css/sb-admin-2.min.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CreateTask from './CreateTask';
import SquadTaskAssignments from './SquadTaskAssignments';
import TaskFormDisplay from './TaskFormDisplay';
import Sidebar from './Sidebar';

function App() {
  const [activeTab, setActiveTab] = useState('createTask');
  const [tasks, setTasks] = useState([]);

  const handleAddTask = (newTask) => {
    setTasks(prevTasks => [...prevTasks, newTask]);
  };

  return (
    <Router>
      <div id="wrapper">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <div id="content-wrapper" className="d-flex flex-column">
          <div className="tab-content mt-3">
            <Routes>
              <Route path="/" element={<CreateTask onTaskCreate={handleAddTask} />} />
              <Route path="/task-overview" element={<TaskFormDisplay />} />
              <Route path="/squad-assignments" element={<SquadTaskAssignments tasks={tasks} />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
