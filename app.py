"""
CampusFix - Flask Web Application
Agile Team Project - SE_CampusFix_Team04
National Taipei University / Software Engineering

Provides REST API and web UI for student campus problem reporting,
tracking, keyword/location search, and staff resolution management.
"""

import os
from flask import Flask, request, jsonify, render_template, session
from database import init_db, create_report, get_report_by_id, get_reports, update_report_status, reset_and_seed

app = Flask(__name__)
# Standard session secret for demo student project
app.secret_key = 'ntpu-campusfix-secret-key-2026'

# Ensure database is initialized on startup
init_db()

DEMO_ACCOUNTS = {
    'student': {
        'email': 'student@ntpu.edu.tw',
        'role': 'student',
        'name': 'Student Demo (Alex Chen - Student)',
        'department': 'Computer Science & Information Engineering'
    },
    'staff': {
        'email': 'staff@ntpu.edu.tw',
        'role': 'staff',
        'name': 'Staff Demo (Officer Lin - Facility Management)',
        'department': 'Office of General Affairs (Facility Division)'
    }
}

@app.before_request
def setup_demo_session():
    """Sets default role to student if not already established."""
    if 'role' not in session:
        session['role'] = 'student'
        session['email'] = DEMO_ACCOUNTS['student']['email']
        session['name'] = DEMO_ACCOUNTS['student']['name']

# ----------------- Page Route -----------------

@app.route('/')
def index():
    """Renders the main single-page application matching NTPU design language."""
    return render_template('index.html')

# ----------------- Auth / Demo Role Routes -----------------

@app.route('/api/auth/current', methods=['GET'])
def get_current_user():
    """Returns the currently active demonstration account and role."""
    role = session.get('role', 'student')
    account_info = DEMO_ACCOUNTS.get(role, DEMO_ACCOUNTS['student'])
    return jsonify({
        'success': True,
        'user': account_info
    })

@app.route('/api/auth/switch', methods=['POST'])
def switch_role():
    """
    Switches demonstration session between 'student' and 'staff'.
    Allows convenient testing of staff-restricted features without full SSO.
    """
    data = request.get_json(silent=True) or {}
    target_role = data.get('role', 'student')
    
    if target_role not in DEMO_ACCOUNTS:
        return jsonify({'success': False, 'error': f'Invalid role: {target_role}'}), 400
        
    session['role'] = target_role
    session['email'] = DEMO_ACCOUNTS[target_role]['email']
    session['name'] = DEMO_ACCOUNTS[target_role]['name']
    
    return jsonify({
        'success': True,
        'message': f'Switched account to {DEMO_ACCOUNTS[target_role]["name"]}',
        'user': DEMO_ACCOUNTS[target_role]
    })

# ----------------- Problem Reporting & Tracking Routes -----------------

@app.route('/api/reports', methods=['GET'])
def list_reports():
    """
    Lists reports with optional keyword search and location filtering.
    Sprint 2 (CF-21):
      - Case-insensitive keyword search in title & description.
      - Location filter.
      - Combined filter behaves as logical AND.
    """
    keyword = request.args.get('keyword', '').strip()
    location = request.args.get('location', '').strip()
    
    reports = get_reports(keyword=keyword, location=location)
    return jsonify({
        'success': True,
        'count': len(reports),
        'reports': reports,
        'applied_filters': {
            'keyword': keyword,
            'location': location
        }
    })

@app.route('/api/reports', methods=['POST'])
def submit_report():
    """
    Submits a new campus problem report.
    Sprint 1 (CF-10): Save title, location, category, description.
    Validation:
      - All 4 required fields must be non-empty strings.
      - Returns field-specific error messages if validation fails.
    """
    data = request.get_json(silent=True) or {}
    
    title = data.get('title', '')
    location = data.get('location', '')
    category = data.get('category', '')
    description = data.get('description', '')
    
    errors = {}
    if not isinstance(title, str) or not title.strip():
        errors['title'] = 'Title is required. Please provide a brief title.'
    if not isinstance(location, str) or not location.strip():
        errors['location'] = 'Campus location is required.'
    if not isinstance(category, str) or not category.strip():
        errors['category'] = 'Category is required.'
    if not isinstance(description, str) or not description.strip():
        errors['description'] = 'Problem description is required.'
        
    if errors:
        return jsonify({
            'success': False,
            'message': 'Validation failed. Please correct the highlighted errors.',
            'errors': errors
        }), 400
        
    new_report = create_report(
        title=title,
        location=location,
        category=category,
        description=description
    )
    
    return jsonify({
        'success': True,
        'message': f'Report {new_report["report_id"]} submitted successfully!',
        'report': new_report
    }), 201

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report_detail(report_id):
    """Retrieves full details of a single report by its ID."""
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({'success': False, 'error': f'Report {report_id} not found.'}), 404
        
    return jsonify({
        'success': True,
        'report': report
    })

# ----------------- Staff Resolution Management Routes -----------------

@app.route('/api/reports/<report_id>/status', methods=['POST'])
def update_status(report_id):
    """
    Updates a report's status and resolution note.
    Sprint 1 & Sprint 2 (CF-30):
      - Restricted to staff role. Student accounts receive 403 Forbidden.
      - Valid statuses: 'Submitted', 'In Progress', 'Resolved'.
      - If status is 'Resolved', a non-empty resolution note is MANDATORY.
    """
    current_role = session.get('role', 'student')
    if current_role != 'staff':
        return jsonify({
            'success': False,
            'error': 'Access denied: Only university staff members are permitted to update report status.'
        }), 403
        
    report = get_report_by_id(report_id)
    if not report:
        return jsonify({'success': False, 'error': f'Report {report_id} not found.'}), 404
        
    data = request.get_json(silent=True) or {}
    new_status = data.get('status', '').strip()
    resolution_note = data.get('resolution_note', '').strip()
    
    valid_statuses = ['Submitted', 'In Progress', 'Resolved']
    if new_status not in valid_statuses:
        return jsonify({
            'success': False,
            'error': f'Invalid status "{new_status}". Allowed statuses: {", ".join(valid_statuses)}'
        }), 400
        
    if new_status == 'Resolved' and not resolution_note:
        return jsonify({
            'success': False,
            'error': 'A resolution note is required when marking a report as Resolved.'
        }), 400
        
    update_report_status(report['id'], new_status, resolution_note)
    updated_report = get_report_by_id(report['id'])
    
    return jsonify({
        'success': True,
        'message': f'Report {updated_report["report_id"]} updated to status "{new_status}".',
        'report': updated_report
    })

# ----------------- Maintenance / Demo Reset -----------------

@app.route('/api/reset-demo', methods=['POST'])
def reset_demo():
    """Resets the SQLite database with fresh seed data for quick class demonstration."""
    reset_and_seed()
    return jsonify({
        'success': True,
        'message': 'Database re-seeded with demo campus reports.'
    })

if __name__ == '__main__':
    reports = get_reports()
    if len(reports) == 0:
        reset_and_seed()
    print("Starting NTPU CampusFix on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
