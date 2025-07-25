# Label Studio App for Crash Narrative Classification
import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database setup
DATABASE = 'crash_narratives.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create table for crash narratives
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crash_narratives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            narrative TEXT NOT NULL,
            severity_label TEXT,
            category_label TEXT,
            weather_condition TEXT,
            time_of_day TEXT,
            vehicle_type TEXT,
            labeled_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            labeled_at TIMESTAMP
        )
    ''')
    
    # Create table for labeling statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labeling_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_narratives INTEGER,
            labeled_narratives INTEGER,
            unlabeled_narratives INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard"""
    conn = get_db_connection()
    
    # Get statistics
    total_count = conn.execute('SELECT COUNT(*) as count FROM crash_narratives').fetchone()['count']
    labeled_count = conn.execute('SELECT COUNT(*) as count FROM crash_narratives WHERE severity_label IS NOT NULL').fetchone()['count']
    unlabeled_count = total_count - labeled_count
    
    # Get recent activities
    recent_labels = conn.execute('''
        SELECT narrative, severity_label, category_label, labeled_by, labeled_at 
        FROM crash_narratives 
        WHERE labeled_at IS NOT NULL 
        ORDER BY labeled_at DESC 
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_count=total_count,
                         labeled_count=labeled_count,
                         unlabeled_count=unlabeled_count,
                         recent_labels=recent_labels)

@app.route('/label')
def label_interface():
    """Labeling interface"""
    conn = get_db_connection()
    
    # Get next unlabeled narrative
    narrative = conn.execute('''
        SELECT * FROM crash_narratives 
        WHERE severity_label IS NULL 
        ORDER BY id 
        LIMIT 1
    ''').fetchone()
    
    conn.close()
    
    if not narrative:
        return redirect(url_for('index'))
    
    return render_template('label_interface.html', narrative=narrative)

@app.route('/submit_label', methods=['POST'])
def submit_label():
    """Submit a label for a narrative"""
    data = request.json
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE crash_narratives 
        SET severity_label = ?, category_label = ?, weather_condition = ?, 
            time_of_day = ?, vehicle_type = ?, labeled_by = ?, labeled_at = ?
        WHERE id = ?
    ''', (
        data['severity_label'],
        data['category_label'],
        data['weather_condition'],
        data['time_of_day'],
        data['vehicle_type'],
        data['labeled_by'],
        datetime.now(),
        data['narrative_id']
    ))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    """Upload crash narrative data"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if file and file.filename.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(file)
            
            # Assume the CSV has a 'narrative' column
            if 'narrative' not in df.columns:
                return jsonify({'error': 'CSV must contain a "narrative" column'})
            
            conn = get_db_connection()
            
            # Insert narratives into database
            for _, row in df.iterrows():
                conn.execute('''
                    INSERT INTO crash_narratives (narrative) 
                    VALUES (?)
                ''', (row['narrative'],))
            
            conn.commit()
            conn.close()
            
            return jsonify({'status': 'success', 'message': f'Uploaded {len(df)} narratives'})
        
        return jsonify({'error': 'Please upload a CSV file'})
    
    return render_template('upload_data.html')

@app.route('/export_labels')
def export_labels():
    """Export labeled data"""
    conn = get_db_connection()
    
    labeled_data = conn.execute('''
        SELECT * FROM crash_narratives 
        WHERE severity_label IS NOT NULL
    ''').fetchall()
    
    conn.close()
    
    # Convert to list of dictionaries
    data = []
    for row in labeled_data:
        data.append(dict(row))
    
    return jsonify(data)

@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    conn = get_db_connection()
    
    # Get label distribution
    severity_distribution = conn.execute('''
        SELECT severity_label, COUNT(*) as count 
        FROM crash_narratives 
        WHERE severity_label IS NOT NULL 
        GROUP BY severity_label
    ''').fetchall()
    
    category_distribution = conn.execute('''
        SELECT category_label, COUNT(*) as count 
        FROM crash_narratives 
        WHERE category_label IS NOT NULL 
        GROUP BY category_label
    ''').fetchall()
    
    conn.close()
    
    return render_template('analytics.html', 
                         severity_distribution=severity_distribution,
                         category_distribution=category_distribution)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
