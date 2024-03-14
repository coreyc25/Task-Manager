import React from 'react';

function TasksOverview() {
    return (
    <div className="row">
      <div className="col-10">
        <div className="card shadow mb-4">
          {/* Card Header - Dropdown */}
          <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 className="m-0 font-weight-bold text-primary">Tasks Overview</h6>
            <div className="dropdown no-arrow">
              <a className="dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i className="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
              </a>
              <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                <div className="dropdown-header">Dropdown Header:</div>
                <a className="dropdown-item" href="#">Action</a>
                <a className="dropdown-item" href="#">Another action</a>
                <div className="dropdown-divider"></div>
                <a className="dropdown-item" href="#">Something else here</a>
              </div>
            </div>
          </div>
          {/* Card Body */}
          <div className="card-body">
            <div className="form">
              <form method="post" action="{{ url_for('createEventSubmit')}}">
                <div className="row mb-3">
                  <div className="col-3">
                    <label className="form-label font-weight-bold">Squads Available</label>
                    <input className="form-control" type="number" name="numSquads" placeholder="1" id="numSquads" step="1" min="1" max="100" required />
                  </div>
                  <div className="col-3">
                    <label className="form-label font-weight-bold">Time Limit</label>
                    <input className="form-control" type="time" name="eName" placeholder="Name" id="eName" required />
                  </div>
                  <div className="col-3">
                    <label className="form-label font-weight-bold">Break Time</label>
                    <input className="form-control" type="time" name="eName" placeholder="Name" id="eName" required />
                  </div>
                  <div className="col-3">
                    <label className="form-label font-weight-bold">Priority</label>
                    <select className="form-control" name="" id="">
                      <option defaultValue value="">Select...</option>
                      <option value="maxTasks">Number of Tasks</option>
                      <option value="maxPriority">Cumulative Priority</option>
                    </select>
                  </div>
                </div>

                <div className="row">
                  <div className="col-12 mx-auto text-center d-flex pt-3 pb-4">
                    <button className="btn btn-primary d-block w-20 mt-2" style={{ marginLeft: "50px" }} type="submit">Optimize</button>
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

export default TasksOverview;
