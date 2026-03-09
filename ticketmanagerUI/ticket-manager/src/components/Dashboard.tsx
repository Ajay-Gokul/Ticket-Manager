import React, { useState, useEffect } from "react";
import { authService, ticketService } from "../services/api";
import { type TicketResponse, StatusMap } from "../types";
import "./Dashboard.css";

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const [tickets, setTickets] = useState<TicketResponse[]>([]);
  const [activeTab, setActiveTab] = useState<
    "my-tickets" | "open-tickets" | "my-tasks"
  >("my-tickets");
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const [newTicket, setNewTicket] = useState({
    Title: "",
    Description: "",
    Priority: "Medium",
  });

  useEffect(() => {
    const initDashboard = async () => {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
        if (userData.Role === "Admin") {
          setActiveTab("open-tickets");
        }
      } catch (err) {
        window.location.href = "/login";
      }
    };
    initDashboard();
  }, []);

  useEffect(() => {
    if (user) {
      loadTickets();
    }
  }, [user, activeTab]);

  const loadTickets = async () => {
    setLoading(true);
    try {
      let data: TicketResponse[] = [];
      if (activeTab === "my-tickets") data = await ticketService.getMyTickets();
      else if (activeTab === "open-tickets")
        data = await ticketService.getUnassignedTickets();
      else if (activeTab === "my-tasks")
        data = await ticketService.getMyTasks();
      setTickets(data);
    } catch (err) {
      console.error("Failed to load tickets");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ticketService.createTicket({ ...newTicket });
      setShowCreateForm(false);
      setNewTicket({ Title: "", Description: "", Priority: "Medium" });
      loadTickets();
    } catch (err) {
      alert("Failed to create ticket");
    }
  };

  const handleAssignToMe = async (ticketId: string) => {
    try {
      await ticketService.assignToMe(ticketId);
      loadTickets();
    } catch (err) {
      alert("Failed to assign ticket");
    }
  };

  const handleStatusUpdate = async (ticketId: string, statusUID: string) => {
    if (!statusUID) return;
    try {
      await ticketService.updateTicket(ticketId, { StatusUID: statusUID });
      loadTickets();
    } catch (err) {
      alert("Failed to update status");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  if (!user) return <div className="loading-screen">Loading...</div>;

  return (
    <div className="dashboard-container">
      {/* 1. Header Section */}
      <header className="dashboard-header">
        <div className="header-left">
          <img src="/logo.png" alt="Logo" className="nav-logo" />
          <h1>Ticket Manager</h1>
        </div>
        <div className="header-right">
          <div className="user-info">
            <div className="profile-avatar">{user.Name.charAt(0)}</div>
            <span className="user-name">{user.Name}</span>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      {/* 2. Navigation Section */}
      <nav className="dashboard-nav">
        <div className="nav-content">
          <div className="tabs-group">
            {user.Role === "User" && (
              <button
                className={`tab ${activeTab === "my-tickets" ? "active" : ""}`}
                onClick={() => setActiveTab("my-tickets")}
              >
                My Tickets
              </button>
            )}
            {user.Role === "Admin" && (
              <>
                <button
                  className={`tab ${activeTab === "open-tickets" ? "active" : ""}`}
                  onClick={() => setActiveTab("open-tickets")}
                >
                  Open Tickets
                </button>
                <button
                  className={`tab ${activeTab === "my-tasks" ? "active" : ""}`}
                  onClick={() => setActiveTab("my-tasks")}
                >
                  My Tasks
                </button>
              </>
            )}
          </div>
          {user.Role === "User" && (
            <button
              className="create-btn"
              onClick={() => setShowCreateForm(true)}
            >
              New Ticket
            </button>
          )}
        </div>
      </nav>

      {/* 3. Main Ticket Section */}
      <main className="dashboard-main">
        {loading ? (
          <div className="loading-spinner">Loading tickets...</div>
        ) : tickets.length === 0 ? (
          <div className="empty-state">
            <p>no ticket</p>
          </div>
        ) : (
          <div className="ticket-grid">
            {tickets.map((ticket) => (
              <div className="ticket-card" key={ticket.UID}>
                <div className="ticket-info">
                  <h3>{ticket.Title}</h3>
                  <p>{ticket.Description}</p>
                </div>

                <div className="meta-group">
                  <span className="meta-label">Priority</span>
                  <span
                    className={`priority-badge ${ticket.Priority.toLowerCase()}`}
                  >
                    {ticket.Priority}
                  </span>
                </div>

                <div className="meta-group">
                  <span className="meta-label">Status</span>
                  <span
                    className={`status-tag ${(StatusMap[(ticket.StatusUID || "").toUpperCase()] || "unknown").toLowerCase()}`}
                  >
                    {StatusMap[(ticket.StatusUID || "").toUpperCase()] || "New"}
                  </span>
                </div>

                <div className="card-actions">
                  {activeTab === "open-tickets" && (
                    <button
                      className="action-link"
                      onClick={() => handleAssignToMe(ticket.UID)}
                    >
                      Claim Ticket
                    </button>
                  )}
                  {activeTab === "my-tasks" && (
                    <select
                      className="status-dropdown"
                      value={(ticket.StatusUID || "").toUpperCase()}
                      onChange={(e) =>
                        handleStatusUpdate(ticket.UID, e.target.value)
                      }
                    >
                      <option value="4FAF6585-8EFC-4AD4-AEDD-159A1D2FF57B">
                        Active
                      </option>
                      <option value="5D95CD40-3755-489C-9978-F1A53D62845E">
                        Closed
                      </option>
                    </select>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* 4. Create Ticket Modal */}
      {showCreateForm && (
        <div className="modal-overlay">
          <div className="modal-card">
            <h2>Create Ticket</h2>
            <form onSubmit={handleCreateTicket}>
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={newTicket.Title}
                  onChange={(e) =>
                    setNewTicket({ ...newTicket, Title: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newTicket.Description}
                  onChange={(e) =>
                    setNewTicket({ ...newTicket, Description: e.target.value })
                  }
                  required
                  rows={4}
                />
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  value={newTicket.Priority}
                  onChange={(e) =>
                    setNewTicket({ ...newTicket, Priority: e.target.value })
                  }
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                </select>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn-submit"
                  onClick={() => setShowCreateForm(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-submit">
                  Submit Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
