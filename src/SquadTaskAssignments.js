import React, { useState } from 'react';
import axios from 'axios';

function SquadTaskAssignments({ tasks }) {
  const [solution, setSolution] = useState(null);
  const [score, setScore] = useState(null);

  

  const generateSolution = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    let endpoint = "http://localhost:8000/api/load-assignments/";
    axios.post(endpoint, formData)
      .then(response => {
        setScore(response.data.score);
        setSolution(response.data.assignments);
      })
      .catch(error => {
        console.error('Error fetching solution:', error);
      });
  };

  return (
    <div className='row ml-4 mr-4'>
      <div className='col-4'>
        <form onSubmit={generateSolution}>
          <div className="mb-3">
            <label
              className="form-label text-primary font-weight-bold">Available Squads</label>
            <input className="form-control"
              type="number" name="squads" placeholder="1"
              id="squads" min={1} step={1}
              required />
          </div>
          <button className="btn btn-success d-block w-20 mt-2" type='submit'>Assign Tasks</button>
        </form>
      </div>
      <div className='col-1'></div>
      <div className="col-4">
        <p className='h3 text-black fw-bold'>
          Priority Score: {score}
        </p>
      </div>
      <div className="row mt-4">
        {solution &&
          Object.keys(solution).map((squadId) => (
            <div className="col-lg-4 mb-4" key={squadId}>
              <div className="card">
                <div className="card-header text-primary fw-bold">Squad {squadId}</div>
                <ul className="list-group list-group-flush">
                  {Object.entries(solution[squadId]).map(([time, task]) => (
                    <li className="list-group-item" key={time}>
                      {`${time}: ${task}`}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
      </div>
    </div>

  );
}

export default SquadTaskAssignments;