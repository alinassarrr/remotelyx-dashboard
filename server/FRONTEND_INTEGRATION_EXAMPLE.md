# Frontend Integration: Job Status Updates

## 🎯 **What We've Built**

The backend now supports manual job status updates with these endpoints:

### **API Endpoints**

- `PATCH /api/v1/jobs/{job_id}/status` - Update job status
- `GET /api/v1/jobs/statuses/available` - Get available statuses
- `PUT /api/v1/jobs/{job_id}` - Full job update

### **Available Statuses**

- **New** (Blue) - Fresh job posting
- **Analyzed** (Green) - Job has been reviewed
- **Matched** (Purple) - Candidate matched
- **In Progress** (Orange) - Interview/negotiation phase
- **Closed** (Gray) - Position filled
- **Rejected** (Red) - Position cancelled

## 🔧 **Frontend Implementation Examples**

### **1. Status Dropdown Component (React/JavaScript)**

```javascript
// Status Update Component
const JobStatusUpdater = ({ jobId, currentStatus, onStatusChange }) => {
  const [statuses, setStatuses] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch available statuses
  useEffect(() => {
    fetch("/api/v1/jobs/statuses/available")
      .then((res) => res.json())
      .then((data) => setStatuses(data.statuses));
  }, []);

  const handleStatusChange = async (newStatus) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/jobs/${jobId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });

      if (response.ok) {
        onStatusChange(newStatus);
        // Show success message
      }
    } catch (error) {
      console.error("Error updating status:", error);
      // Show error message
    } finally {
      setLoading(false);
    }
  };

  return (
    <select
      value={currentStatus}
      onChange={(e) => handleStatusChange(e.target.value)}
      disabled={loading}
      className="status-select"
    >
      {statuses.map((status) => (
        <option key={status.value} value={status.value}>
          {status.label}
        </option>
      ))}
    </select>
  );
};
```

### **2. Status Badge with Update (HTML/CSS)**

```html
<!-- Status Badge with Update Functionality -->
<div class="job-status-container">
  <div class="status-badge" data-status="New">
    <span class="status-text">New</span>
    <button class="status-edit-btn" onclick="showStatusEditor('job-123')">
      ✏️
    </button>
  </div>
</div>

<!-- Status Editor Modal -->
<div id="statusEditor" class="modal" style="display: none;">
  <div class="modal-content">
    <h3>Update Job Status</h3>
    <select id="statusSelect" class="status-dropdown">
      <option value="New">New</option>
      <option value="Analyzed">Analyzed</option>
      <option value="Matched">Matched</option>
      <option value="In Progress">In Progress</option>
      <option value="Closed">Closed</option>
      <option value="Rejected">Rejected</option>
    </select>
    <div class="modal-actions">
      <button onclick="updateJobStatus()">Update</button>
      <button onclick="closeStatusEditor()">Cancel</button>
    </div>
  </div>
</div>
```

### **3. Streamlit Integration (Python)**

```python
import streamlit as st
import requests

def update_job_status(job_id: str, new_status: str):
    """Update job status via API."""
    try:
        response = requests.patch(
            f"http://localhost:8000/api/v1/jobs/{job_id}/status",
            json={"status": new_status}
        )
        if response.status_code == 200:
            st.success(f"Status updated to {new_status}")
            return True
        else:
            st.error(f"Failed to update status: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def render_job_with_status_update(job):
    """Render job card with status update functionality."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"**{job['title']}** at {job['company']}")
        st.write(f"Location: {job['location']}")
        st.write(f"Salary: {job['salary']}")

    with col2:
        current_status = job.get('status', 'New')
        new_status = st.selectbox(
            "Status",
            ["New", "Analyzed", "Matched", "In Progress", "Closed", "Rejected"],
            index=["New", "Analyzed", "Matched", "In Progress", "Closed", "Rejected"].index(current_status),
            key=f"status_{job['id']}"
        )

        if new_status != current_status:
            if st.button("Update Status", key=f"update_{job['id']}"):
                update_job_status(job['id'], new_status)
                st.rerun()
```

### **4. CSS Styling for Status Badges**

```css
/* Status Badge Styles */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
}

.status-badge[data-status="New"] {
  background-color: #dbeafe;
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.status-badge[data-status="Analyzed"] {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #6ee7b7;
}

.status-badge[data-status="Matched"] {
  background-color: #ede9fe;
  color: #5b21b6;
  border: 1px solid #a78bfa;
}

.status-badge[data-status="In Progress"] {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #fbbf24;
}

.status-badge[data-status="Closed"] {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.status-badge[data-status="Rejected"] {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.status-edit-btn {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.status-edit-btn:hover {
  opacity: 1;
}
```

## 🚀 **Integration Steps**

### **1. Add Status Field to Job Data**

Make sure your frontend job objects include a `status` field.

### **2. Implement Status Update UI**

- Add status dropdowns to job cards
- Create status update buttons/forms
- Show current status with visual indicators

### **3. Connect to Backend API**

- Call the status update endpoint when status changes
- Handle success/error responses
- Update local state after successful updates

### **4. Add Visual Feedback**

- Show loading states during updates
- Display success/error messages
- Update status badges immediately after changes

## 📱 **User Experience Features**

- **Real-time Updates**: Status changes reflect immediately
- **Visual Status Indicators**: Color-coded status badges
- **Bulk Status Updates**: Update multiple jobs at once
- **Status History**: Track status changes over time
- **Permission-based Updates**: Control who can change statuses

## 🔄 **Status Workflow Example**

```
New → Analyzed → Matched → In Progress → Closed
  ↓
Rejected (if position is cancelled)
```

This creates a clear recruitment pipeline that users can manage through the frontend interface!
