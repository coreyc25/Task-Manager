import React, { useState } from 'react';

function CreateTask({ onTaskCreate }) {
  const [taskName, setTaskName] = useState('');
  const [taskPriority, setTaskPriority] = useState('');
  const [taskDependencies, setTaskDependencies] = useState('');
  const [squadsNeeded, setSquadsNeeded] = useState('');
  const [timeNeeded, setTimeNeeded] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    const newTask = {
      name: taskName,
      priority: taskPriority,
      dependencies: taskDependencies.split(',').map(dep => dep.trim()),
      squad: squadsNeeded,
      time: timeNeeded,
    };
    onTaskCreate(newTask);
    resetForm();
  };

  // Function to reset form fields
  const resetForm = () => {
    setTaskName('');
    setTaskPriority('');
    setTaskDependencies('');
    setSquadsNeeded('');
    setTimeNeeded('');
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="mb-3">
        <div className="mb-3">
          <label htmlFor="taskName" className="form-label">Task Name:</label>
          <input
            type="text"
            className="form-control"
            id="taskName"
            value={taskName}
            onChange={(e) => setTaskName(e.target.value)}
          />
        </div>
        {/* Repeat the structure for other fields */}
        <div className="mb-3">
          <label htmlFor="taskPriority" className="form-label">Task Priority:</label>
          <input
            type="number"
            className="form-control"
            id="taskPriority"
            value={taskPriority}
            onChange={(e) => setTaskPriority(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="taskDependencies" className="form-label">Task Dependencies (comma-separated):</label>
          <input
            type="text"
            className="form-control"
            id="taskDependencies"
            value={taskDependencies}
            onChange={(e) => setTaskDependencies(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="squadsNeeded" className="form-label">Squads Needed:</label>
          <input
            type="number"
            className="form-control"
            id="squadsNeeded"
            value={squadsNeeded}
            onChange={(e) => setSquadsNeeded(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="timeNeeded" className="form-label">Time Needed:</label>
          <input
            type="time"
            className="form-control"
            id="timeNeeded"
            value={timeNeeded}
            onChange={(e) => setTimeNeeded(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary me-2">Add Task</button>
        <button type="button" className="btn btn-secondary" onClick={resetForm}>Cancel</button>
      </form>
    </div>
  );
}

export default CreateTask;
