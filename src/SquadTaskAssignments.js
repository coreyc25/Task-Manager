import React from 'react';

function SquadTaskAssignments({ tasks }) {
  return (
    <div className="table-responsive">
      <table className="table">
        <thead>
          <tr>
            <th>Task Name</th>
            <th>Priority</th>
            <th>Dependencies</th>
            <th>Squad Assigned</th>
            <th>Time Needed</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task, index) => (
            <tr key={index}>
              <td>{task.name}</td>
              <td>{task.priority}</td>
              <td>{task.dependencies.join(', ')}</td>
              <td>{task.squad}</td>
              <td>{task.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SquadTaskAssignments;
