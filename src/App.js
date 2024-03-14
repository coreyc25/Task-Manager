import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Import Bootstrap JS
import CreateTask from './CreateTask';
import TasksOverview from './TasksOverview';

function App() {
  return (
    <div className="App">
      <TasksOverview/>
      <CreateTask />
    </div>
  );
}

export default App;
