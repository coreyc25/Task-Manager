import React from 'react';
import axios from 'axios';

const TasksTable = ({ tasksData, fetchTasks }) => {
  
  const handleDelete = async (taskId) => {
    try {
      const response = await axios.post('http://localhost:8000/api/delete-task/', { id: taskId });
      console.log(response.data);
      fetchTasks();
    } catch (error) {
      console.error('Error adding document:', error);
    }
  };

  return (
    <div>
      <h2 className='text-primary font-weight-bold'>Tasks</h2>
      <div className="table-responsive mr-2">
        <table className="table table-bordered table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Priority</th>
              <th>Squads</th>
              <th>Dependencies</th>
              <th>Time</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            {tasksData.map((item) => (
              <tr key={item._id}>
                <td>{item.task_name}</td>
                <td>{item.priority}</td>
                <td>{item.squads}</td>
                <td>{item.depends}</td>
                <td>{item.hours} hours {item.minutes} minutes</td>
                <td><button type="button"
                  onClick={() => handleDelete(item._id)}
                  className="btn btnMaterial btn-flat accent btnNoBorders checkboxHover"><i
                    className="fas fa-trash btnNoBorders"
                    style={{ color: '#DC3545' }}></i></button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
export default TasksTable;