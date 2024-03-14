import React from 'react';

function CreateTask() {
    return (
        <div class="row">
            <div class="col-6">
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6
                            class="m-0 font-weight-bold text-primary">Create
                            Tasks</h6>
                    </div>
                    <div class="card-body">
                        <div class="form">
                            <form method="post"
                                action="{{ url_for('createEventSubmit')}}">
                                <div class="mb-3">
                                    <label
                                        class="form-label form-label font-weight-bold">Task
                                        Name</label>
                                    <input class="form-control form-control form-control"
                                        type="text" name="eName" placeholder="Name"
                                        id="eName"
                                        required /></div>
                                <div class="mb-3">
                                    <label
                                        class="form-label form-label font-weight-bold">Task
                                        Priority</label>
                                    <input class="form-control form-control form-control"
                                        type="number" name="eName" placeholder="100"
                                        id="eName"
                                        required /></div>
                                <div class="mb-3">
                                    <label
                                        class="form-label form-label font-weight-bold">Task
                                        Dependencies</label>
                                    <input class="form-control form-control form-control"
                                        type="text" name="eName" placeholder=""
                                        id="eName"
                                        required />
                                </div>
                                <div class="mb-3">
                                    <label
                                        class="form-label form-label font-weight-bold">Squads
                                        Needed</label>
                                    <input class="form-control form-control form-control"
                                        type="number" name="eName" placeholder="1"
                                        id="eName"
                                        required />
                                </div>
                                <div class="mb-3">
                                    <label
                                        class="form-label form-label font-weight-bold">Time
                                        Needed</label>
                                    <input class="form-control form-control form-control"
                                        type="time" name="eName"
                                        id="eName"
                                        required />
                                </div>
                                <div class="row">
                                    <div
                                        class="col-12 mx-auto text-center d-flex pt-3 pb-4">
                                        <a href="/events-table">
                                            <button type="button"
                                                class="btn btn-light d-block w-100 mt-2">Cancel</button>
                                        </a>
                                        <button class="btn btn-primary d-block w-20 mt-2"
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