import React, { useState } from 'react';
import axios from 'axios';

const CreateTask = ({ fetchTasks }) => {
    const [taskData, setTaskData] = useState({
        // Initialize form data state
        task_name: '',
        priority: '',
        depends: '',
        squads: '',
        hours: '',
        minutes: '',
    });

    const handleChange = (e) => {
        // Update form data state when input values change
        setTaskData({
            ...taskData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/add-task/', taskData);
            console.log(response.data); // Log response from the server
            setTaskData({
                task_name: '',
                priority: '',
                depends: '',
                squads: '',
                hours: '',
                minutes: '',
            });
            fetchTasks();
        } catch (error) {
            console.error('Error adding document:', error);
        }
    };

    const handleCancel = (e) => {
        // Update form data state when input values change
        setTaskData({
            task_name: '',
            priority: '',
            depends: '',
            squads: '',
            hours: '',
            minutes: '',
        });
    };

    return (
        <div className="row">
            <div className="col-6">
                <div className="card shadow mb-4">
                    <div className="card-header py-3">
                        <h6
                            className="m-0 font-weight-bold text-primary">Create
                            Task</h6>
                    </div>
                    <div className="card-body">

                        <div className="form">
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label
                                        className="form-label font-weight-bold">Task
                                        Name</label>
                                    <input className="form-control"
                                        type="text" name="task_name" placeholder="Name"
                                        id="taskName" value={taskData.task_name} onChange={handleChange}
                                        required /></div>
                                <div className="mb-3">
                                    <label
                                        className="form-label font-weight-bold">Task
                                        Priority</label>
                                    <input className="form-control"
                                        type="number" name="priority" placeholder="1-100"
                                        id="priority" value={taskData.priority} onChange={handleChange}
                                        required /></div>
                                <div className="mb-3">
                                    <label
                                        className="form-label font-weight-bold">Task
                                        Dependencies</label>
                                    <label className='ml-1 font-italic'>(List task names separated by commas e.g. Task 1, Task 2)</label>
                                    <textarea className='form-control' name='depends' rows={4} placeholder='Task 1, Task 2' 
                                    id='depends' value={taskData.depends} onChange={handleChange}></textarea>
                                </div>
                                <div className="mb-3">
                                    <label
                                        className="form-label font-weight-bold">Squads
                                        Needed</label>
                                    <input className="form-control"
                                        type="number" name="squads" placeholder="1"
                                        id="squads" value={taskData.squads} onChange={handleChange}
                                        required />
                                </div>
                                <div className="row mb-3">
                                    <div className="col-6">
                                        <label
                                            className="form-label font-weight-bold">Hours</label>
                                        <input className="form-control" type="number" id="hours" name="hours" min="0" max="24" step="1"
                                            value={taskData.hours} onChange={handleChange} required />
                                    </div>
                                    <div className="col-6">
                                        <label
                                            className="form-label font-weight-bold">Minutes</label>
                                        <input className="form-control" type="number" id="minutes" name="minutes" min="0" max="45" step="15"
                                            value={taskData.minutes} onChange={handleChange} required />
                                    </div>


                                </div>
                                <div className="row">
                                    <div
                                        className="col-12 mx-auto text-center d-flex pt-3 pb-4">
                                        <div className='col-2'>
                                        <button type="button" onClick={handleCancel}
                                            className="btn btn-danger d-block w-100 mt-2">Cancel</button>
                                        </div>
                                        
                                        <button className="btn btn-success d-block w-20 mt-2 ml-3"
                                            type="submit">Add Task</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateTask;