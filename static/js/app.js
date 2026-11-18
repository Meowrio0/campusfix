/**
 * CampusFix - Student JavaScript Frontend
 * National Taipei University / Software Engineering Team 04
 * 
 * Clean Institutional Design (No AI-like pastel pill bubbles)
 * Features:
 *  - Sprint 1: Form validation, problem submission, unique ID, status display, report tracking.
 *  - Sprint 2: Case-insensitive search, location filter, combined AND logic, staff resolution note enforcement.
 */

// Application State
let currentRole = 'student';
let currentUser = null;
let currentReports = [];
let activeTab = 'tab-search-track';

// On Document Ready
document.addEventListener('DOMContentLoaded', () => {
    initApp();

    // Close mega dropdown when clicking outside
    document.addEventListener('click', (e) => {
        const dropdown = document.getElementById('ntpu-mega-menu');
        const trigger = document.querySelector('.dropdown-trigger');
        if (dropdown && !dropdown.contains(e.target) && !trigger.contains(e.target)) {
            dropdown.classList.add('d-none');
        }
    });
});

async function initApp() {
    await fetchCurrentUser();
    await loadReports();
}

// ----------------- Header Mega Menu -----------------

function toggleDropdown() {
    const dropdown = document.getElementById('ntpu-mega-menu');
    if (dropdown) {
        dropdown.classList.toggle('d-none');
    }
}

// ----------------- Authentication & Role Switching -----------------

async function fetchCurrentUser() {
    try {
        const res = await fetch('/api/auth/current');
        const data = await res.json();
        if (data.success) {
            currentUser = data.user;
            currentRole = currentUser.role;
            updateUserRoleUI();
        }
    } catch (err) {
        console.error('Failed to fetch user session:', err);
    }
}

async function toggleRole() {
    const nextRole = (currentRole === 'student') ? 'staff' : 'student';
    const payload = { role: nextRole };
    if (nextRole === 'staff') {
        const password = window.prompt('Enter the staff password to switch to the staff account:');
        if (password === null) {
            return; // User cancelled the prompt
        }
        payload.password = password;
    }
    try {
        const res = await fetch('/api/auth/switch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            currentUser = data.user;
            currentRole = currentUser.role;
            updateUserRoleUI();
            showAlert(`Switched active account to: ${currentUser.name}`, 'info');
            loadReports(); // Refresh tables with updated action permissions
        } else {
            showAlert(data.error || 'Role switch was refused.', 'danger');
        }
    } catch (err) {
        showAlert('Failed to switch demonstration role. Please try again.', 'danger');
    }
}

function updateUserRoleUI() {
    const badge = document.getElementById('current-user-badge');
    const switchBtn = document.getElementById('btn-switch-role');
    const warningBox = document.getElementById('staff-restriction-warning');
    const staffRoleTag = document.getElementById('staff-portal-role-tag');
    const userName = document.getElementById('current-user-name');
    const resetCard = document.getElementById('card-nav-reset');

    if (userName && currentUser) {
        userName.textContent = currentUser.name.split(' (')[0];
    }

    if (currentRole === 'staff') {
        if (badge) {
            badge.className = 'user-role-label role-staff-label';
            badge.textContent = 'Staff';
        }
        if (switchBtn) switchBtn.textContent = 'Switch to Student';
        if (warningBox) warningBox.classList.add('d-none');
        if (staffRoleTag) staffRoleTag.textContent = 'Facility Access: Authorized';
        if (resetCard) {
            resetCard.style.opacity = '1';
            resetCard.style.cursor = 'pointer';
            resetCard.title = 'Restore clean seed records';
        }
    } else {
        if (badge) {
            badge.className = 'user-role-label role-student-label';
            badge.textContent = 'Student';
        }
        if (switchBtn) switchBtn.textContent = 'Switch to Staff';
        if (warningBox) warningBox.classList.remove('d-none');
        if (staffRoleTag) staffRoleTag.textContent = 'Access: Student (Read-Only)';
        if (resetCard) {
            resetCard.style.opacity = '0.55';
            resetCard.style.cursor = 'not-allowed';
            resetCard.title = 'Staff Role Required';
        }
    }
}

// ----------------- Navigation Tabs & Service Cards -----------------

function switchTab(tabId) {
    activeTab = tabId;

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        if (pane.id === tabId) {
            pane.classList.add('active');
        } else {
            pane.classList.remove('active');
        }
    });

    // Update top 4-column service cards active indicator
    const cardSearch = document.getElementById('card-nav-search');
    const cardReport = document.getElementById('card-nav-report');
    const cardStaff = document.getElementById('card-nav-staff');

    if (cardSearch) cardSearch.classList.remove('active');
    if (cardReport) cardReport.classList.remove('active');
    if (cardStaff) cardStaff.classList.remove('active');

    if (tabId === 'tab-search-track' && cardSearch) {
        cardSearch.classList.add('active');
    } else if (tabId === 'tab-report' && cardReport) {
        cardReport.classList.add('active');
    } else if (tabId === 'tab-staff' && cardStaff) {
        cardStaff.classList.add('active');
    }

    // Scroll smoothly to main content
    const mainEl = document.getElementById('main-content');
    if (mainEl) {
        mainEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Auto-refresh when entering search or staff tab
    if (tabId === 'tab-search-track' || tabId === 'tab-staff') {
        loadReports();
    }
}

// ----------------- Load & Filter Reports (Sprint 2 Feature) -----------------

async function loadReports() {
    const keyword = document.getElementById('search-keyword')?.value.trim() || '';
    const location = document.getElementById('filter-location')?.value.trim() || '';

    const params = new URLSearchParams();
    if (keyword) params.append('keyword', keyword);
    if (location) params.append('location', location);

    try {
        const res = await fetch(`/api/reports?${params.toString()}`);
        const data = await res.json();

        if (data.success) {
            currentReports = data.reports;
            renderReportsTable(currentReports);
            renderStaffTable(currentReports);
            
            const countText = document.getElementById('results-count-text');
            if (countText) {
                if (keyword || location) {
                    countText.textContent = `(${data.count} report${data.count === 1 ? '' : 's'} matching criteria)`;
                } else {
                    countText.textContent = `(Total: ${data.count} reports)`;
                }
            }
        }
    } catch (err) {
        console.error('Error fetching reports:', err);
    }
}

function handleSearchKeyUp(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
}

function performSearch() {
    loadReports();
}

function resetFilters() {
    const kwInput = document.getElementById('search-keyword');
    const locInput = document.getElementById('filter-location');
    if (kwInput) kwInput.value = '';
    if (locInput) locInput.value = '';
    loadReports();
}

// ----------------- Render Tables (No AI Bubble Pills) -----------------

function getStatusBadgeHtml(status) {
    if (status === 'Submitted') {
        return `<span class="status-indicator status-submitted"><span class="status-bullet"></span>Submitted</span>`;
    } else if (status === 'In Progress') {
        return `<span class="status-indicator status-in-progress"><span class="status-bullet"></span>In Progress</span>`;
    } else if (status === 'Resolved') {
        return `<span class="status-indicator status-resolved"><span class="status-bullet"></span>Resolved</span>`;
    }
    return `<span class="status-indicator">${escapeHtml(status)}</span>`;
}

function renderReportsTable(reports) {
    const tbody = document.getElementById('reports-tbody');
    const emptyMsg = document.getElementById('no-reports-msg');
    const table = document.getElementById('reports-table');

    if (!tbody) return;

    if (!reports || reports.length === 0) {
        tbody.innerHTML = '';
        table.classList.add('d-none');
        emptyMsg.classList.remove('d-none');
        return;
    }

    table.classList.remove('d-none');
    emptyMsg.classList.add('d-none');

    tbody.innerHTML = reports.map(r => `
        <tr>
            <td><span class="table-id-badge">${escapeHtml(r.report_id)}</span></td>
            <td>
                <div style="font-weight: 600; color: #111827;">${escapeHtml(r.title)}</div>
                <div class="text-muted" style="font-size: 12px; margin-top: 2px; line-height: 1.4;">
                    ${escapeHtml(r.description.substring(0, 65))}${r.description.length > 65 ? '...' : ''}
                </div>
            </td>
            <td><span style="color: #374151; font-weight: 500;">${escapeHtml(r.location)}</span></td>
            <td><span style="color: #4B5563;">${escapeHtml(r.category)}</span></td>
            <td>${getStatusBadgeHtml(r.status)}</td>
            <td class="text-muted" style="font-size: 12.5px;">${escapeHtml(r.created_at)}</td>
            <td>
                <button class="btn-ntpu-outline btn-sm" onclick="openDetailModal('${r.report_id}')">
                    View Details
                </button>
            </td>
        </tr>
    `).join('');
}

function renderStaffTable(reports) {
    const tbody = document.getElementById('staff-table-tbody');
    if (!tbody) return;

    if (!reports || reports.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No campus problem reports recorded yet.</td></tr>`;
        return;
    }

    const isStaff = (currentRole === 'staff');

    tbody.innerHTML = reports.map(r => `
        <tr>
            <td><span class="table-id-badge">${escapeHtml(r.report_id)}</span></td>
            <td>
                <div style="font-weight: 600; color: #111827;">${escapeHtml(r.title)}</div>
                <div class="text-muted" style="font-size: 12px;">Building: ${escapeHtml(r.location)}</div>
            </td>
            <td><span style="color: #4B5563;">${escapeHtml(r.category)}</span></td>
            <td>${getStatusBadgeHtml(r.status)}</td>
            <td>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <button class="btn-ntpu-outline btn-sm" onclick="openDetailModal('${r.report_id}')">
                        Details
                    </button>
                    ${isStaff ? `
                        <button class="btn-ntpu-accent btn-sm" onclick="openStatusModal('${r.report_id}')">
                            Update Progress
                        </button>
                    ` : `
                        <button class="btn-ntpu-outline btn-sm" disabled title="Staff Role Required" style="opacity: 0.55; cursor: not-allowed;">
                            Staff Required
                        </button>
                    `}
                </div>
            </td>
        </tr>
    `).join('');
}

// ----------------- Submit Report (Sprint 1 Feature) -----------------

function clearFormErrors() {
    ['title', 'location', 'category', 'description'].forEach(field => {
        const errEl = document.getElementById(`error-${field}`);
        const inputEl = document.getElementById(`form-${field}`);
        if (errEl) errEl.textContent = '';
        if (inputEl) inputEl.classList.remove('is-invalid');
    });
}

function resetReportForm() {
    const form = document.getElementById('report-form');
    if (form) form.reset();
    clearFormErrors();
}

async function handleReportSubmit(e) {
    e.preventDefault();
    clearFormErrors();

    const title = document.getElementById('form-title').value.trim();
    const location = document.getElementById('form-location').value.trim();
    const category = document.getElementById('form-category').value.trim();
    const description = document.getElementById('form-description').value.trim();

    // Client-side validation check
    const MAX_TITLE_LENGTH = 100; // Part A: must match MAX_TITLE_LENGTH in app.py
    let hasError = false;
    if (!title) {
        setFieldError('title', 'Title is required. Please provide a brief title.');
        hasError = true;
    } else if (title.length > MAX_TITLE_LENGTH) {
        setFieldError('title', `Title must be ${MAX_TITLE_LENGTH} characters or fewer.`);
        hasError = true;
    }
    if (!location) {
        setFieldError('location', 'Campus location is required.');
        hasError = true;
    }
    if (!category) {
        setFieldError('category', 'Category is required.');
        hasError = true;
    }
    if (!description) {
        setFieldError('description', 'Problem description is required.');
        hasError = true;
    }

    if (hasError) return;

    const btnSubmit = document.getElementById('btn-submit-report');
    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Submitting report...';

    try {
        const res = await fetch('/api/reports', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, location, category, description })
        });
        const data = await res.json();

        if (res.status === 201 && data.success) {
            showAlert(`Report submitted successfully! Unique ID: <strong>${data.report.report_id}</strong> (Status: ${data.report.status})`, 'success');
            resetReportForm();
            await loadReports();
            switchTab('tab-search-track');
            setTimeout(() => {
                openDetailModal(data.report.report_id);
            }, 300);
        } else if (res.status === 400 && data.errors) {
            for (const [key, msg] of Object.entries(data.errors)) {
                setFieldError(key, msg);
            }
            showAlert('Form validation failed. Please correct the highlighted errors.', 'danger');
        } else {
            showAlert(data.message || 'Submission failed. Please contact facility administrator.', 'danger');
        }
    } catch (err) {
        showAlert('Network error: unable to reach CampusFix server.', 'danger');
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Submit Problem Report';
    }
}

function setFieldError(field, message) {
    const errEl = document.getElementById(`error-${field}`);
    const inputEl = document.getElementById(`form-${field}`);
    if (errEl) errEl.textContent = message;
    if (inputEl) inputEl.classList.add('is-invalid');
}

// ----------------- View Details Modal -----------------

function openDetailModal(reportId) {
    const report = currentReports.find(r => r.report_id === reportId);
    if (!report) return;

    document.getElementById('modal-report-id').textContent = `Report Details: ${report.report_id}`;
    
    const body = document.getElementById('modal-content-body');
    body.innerHTML = `
        <div class="detail-grid">
            <div class="detail-item">
                <div class="detail-label">Report ID</div>
                <div class="detail-value"><span class="table-id-badge">${escapeHtml(report.report_id)}</span></div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Current Status</div>
                <div class="detail-value">${getStatusBadgeHtml(report.status)}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Campus Location</div>
                <div class="detail-value">${escapeHtml(report.location)}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Category</div>
                <div class="detail-value">${escapeHtml(report.category)}</div>
            </div>
            <div class="detail-item detail-full-width">
                <div class="detail-label">Report Title</div>
                <div class="detail-value" style="font-size: 14px; font-weight: 700; color: #111827;">${escapeHtml(report.title)}</div>
            </div>
            <div class="detail-item detail-full-width">
                <div class="detail-label">Detailed Description</div>
                <div class="detail-value" style="white-space: pre-line; line-height: 1.6; margin-top: 4px; color: #374151;">
                    ${escapeHtml(report.description)}
                </div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Submitted At</div>
                <div class="detail-value text-muted">${escapeHtml(report.created_at)}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Last Updated</div>
                <div class="detail-value text-muted">${escapeHtml(report.updated_at)}</div>
            </div>
        </div>

        ${report.resolution_note ? `
            <div class="resolution-box">
                <h5>Official Staff Resolution Note</h5>
                <div class="resolution-text">${escapeHtml(report.resolution_note)}</div>
            </div>
        ` : ''}
    `;

    document.getElementById('detail-modal').classList.remove('d-none');
}

function closeDetailModal() {
    document.getElementById('detail-modal').classList.add('d-none');
}

function handleModalBackdropClick(e) {
    if (e.target.id === 'detail-modal') {
        closeDetailModal();
    }
}

// ----------------- Staff Status Update Modal & Logic -----------------

function openStatusModal(reportId) {
    if (currentRole !== 'staff') {
        showAlert('Access Denied: Only staff members are permitted to update report status. Switch role in top header.', 'warning');
        return;
    }

    const report = currentReports.find(r => r.report_id === reportId);
    if (!report) return;

    document.getElementById('update-modal-report-id').value = report.report_id;
    document.getElementById('update-modal-summary').innerHTML = `
        <strong>[${escapeHtml(report.report_id)}]</strong> ${escapeHtml(report.title)} 
        <br><small class="text-muted">${escapeHtml(report.location)} | ${escapeHtml(report.category)}</small>
    `;

    document.getElementById('update-new-status').value = report.status;
    document.getElementById('update-resolution-note').value = report.resolution_note || '';
    document.getElementById('error-resolution-note').textContent = '';

    handleTargetStatusChange();
    document.getElementById('status-update-modal').classList.remove('d-none');
}

function handleTargetStatusChange() {
    const status = document.getElementById('update-new-status').value;
    const star = document.getElementById('note-required-star');
    const help = document.getElementById('note-help-text');

    if (status === 'Resolved') {
        star.style.display = 'inline';
        help.textContent = 'Per requirements, marking a report as Resolved mandates a non-empty resolution note.';
    } else {
        star.style.display = 'none';
        help.textContent = 'Optional intermediate notes (e.g., Replacement parts ordered; technician dispatched).';
    }
}

function closeStatusModal() {
    document.getElementById('status-update-modal').classList.add('d-none');
}

function handleStatusModalBackdropClick(e) {
    if (e.target.id === 'status-update-modal') {
        closeStatusModal();
    }
}

async function submitStatusUpdate() {
    const reportId = document.getElementById('update-modal-report-id').value;
    const newStatus = document.getElementById('update-new-status').value;
    const resolutionNote = document.getElementById('update-resolution-note').value.trim();
    const errEl = document.getElementById('error-resolution-note');
    errEl.textContent = '';

    // Frontend validation per handout requirement:
    // "Require a resolution note when resolving a report."
    if (newStatus === 'Resolved' && !resolutionNote) {
        errEl.textContent = 'A resolution note is required when resolving a report.';
        return;
    }

    try {
        const res = await fetch(`/api/reports/${encodeURIComponent(reportId)}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                status: newStatus,
                resolution_note: resolutionNote
            })
        });

        const data = await res.json();

        if (res.status === 200 && data.success) {
            closeStatusModal();
            showAlert(`Report ${reportId} successfully updated to status "${newStatus}".`, 'success');
            await loadReports();
        } else if (res.status === 403) {
            showAlert(data.error || 'Access denied: Staff authorization required.', 'danger');
        } else {
            errEl.textContent = data.error || 'Failed to update status. Please verify inputs.';
        }
    } catch (err) {
        errEl.textContent = 'Network communication error while saving status.';
    }
}

// ----------------- Seed & Reset Helper -----------------

async function resetDemoData() {
    if (!confirm('Reset database to clean initial demonstration records?')) return;

    try {
        const res = await fetch('/api/reset-demo', { method: 'POST' });
        const data = await res.json();
        if (res.status === 200 && data.success) {
            showAlert('Demonstration database reset successfully.', 'info');
            await loadReports();
        } else if (res.status === 403) {
            showAlert(data.error || 'Access denied: Staff authorization required.', 'danger');
        } else {
            showAlert(data.error || 'Failed to reset demo data.', 'danger');
        }
    } catch (err) {
        showAlert('Failed to reset demo data.', 'danger');
    }
}

// ----------------- Alert / Toast Utility -----------------

function showAlert(message, type = 'info') {
    const container = document.getElementById('alert-container');
    if (!container) return;

    const alert = document.createElement('div');
    alert.className = `alert-box alert-${type}`;
    alert.innerHTML = `
        <div class="alert-content" style="flex: 1;">${message}</div>
        <button style="background: none; border: none; font-size: 18px; cursor: pointer; color: inherit;" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.prepend(alert);

    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 6000);
}

// Simple HTML escaper to prevent XSS in student code
function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
