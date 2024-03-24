import React, { useState } from 'react';

function Sidebar() {
    const [activeTab, setActiveTab] = useState('createTask');

    return (
        <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            {/* Sidebar - Brand */}
            <a className="sidebar-brand d-flex align-items-center justify-content-center" href="task-overview">
                <div className="sidebar-brand-icon rotate-n-15">
                    <i className="fas fa-tachometer-alt"></i>
                </div>
                <div className="sidebar-brand-text mx-3">Task Manager</div>
            </a>

            {/* Divider */}
            <hr className="sidebar-divider my-0" />
            <li className="nav-item active">
                <a className="nav-link" href="task-overview">
                    <span>Task Overview</span>
                </a>
            </li>
            <li className="nav-item active">
                <a className="nav-link" href="squad-assignments">
                    <span>Squad Assignments</span>
                </a>
            </li>
            

            <li className="nav-item">
                <button
                    className={`nav-link ${activeTab === 'squadTasks' ? 'active' : ''}`}
                    onClick={() => setActiveTab('squadTasks')}
                >                </button>
            </li>
        </ul>


    );
}

export default Sidebar;
