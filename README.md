# Crash Narrative Classification - Label Studio Project

A comprehensive data labeling application for crash narrative classification using Flask and web technologies.


https://github.com/user-attachments/assets/4c880924-d38a-4cc0-b0bf-ac3f7f736338


## Features

- **Interactive Labeling Interface**: User-friendly interface for labeling crash narratives with multiple classification categories
- **Data Upload**: Easy CSV file upload functionality for bulk data import
- **Real-time Analytics**: Visual analytics dashboard with charts and statistics
- **Progress Tracking**: Monitor labeling progress with completion metrics
- **Data Export**: Export labeled data in various formats
- **Multi-category Classification**:
  - Crash Severity (Minor, Moderate, Major, Fatal)
  - Crash Category (Vehicle Collision, Pedestrian, Single Vehicle, etc.)
  - Weather Conditions (Clear, Rain, Snow, Fog, Unknown)
  - Time of Day (Morning, Afternoon, Evening, Night, Unknown)
  - Vehicle Type (Car, Truck, SUV, Motorcycle, Bicycle, Other)

## Installation

1. **Activate your virtual environment**:
   ```powershell
   cd "c:\Users\hp\Downloads\labeling Task"
   .\env\Scripts\Activate.ps1
   ```

2. **Install required dependencies**:
   ```powershell
   pip install flask pandas sqlite3
   ```

3. **Run the application**:
   ```powershell
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### 1. Upload Data
- Go to the "Upload Data" section
- Upload a CSV file with a "narrative" column containing crash descriptions
- The system will import all narratives for labeling

### 2. Label Narratives
- Click "Label Data" to start the labeling process
- Read each crash narrative carefully
- Select appropriate labels for each category:
  - **Severity**: How severe was the crash?
  - **Category**: What type of crash occurred?
  - **Weather**: What were the weather conditions?
  - **Time**: When did the crash occur?
  - **Vehicle**: What was the primary vehicle type?
- Enter your name as the labeler
- Submit the labels to save and move to the next narrative

### 3. View Analytics
- Access the "Analytics" dashboard to see:
  - Distribution of crash severities
  - Breakdown of crash categories
  - Labeling progress statistics
  - Visual charts and graphs

### 4. Export Data
- Export labeled data as JSON
- Download analytics reports
- Access raw data for further analysis

## File Structure

```
labeling Task/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── crash_narratives.db   # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── dashboard.html    # Main dashboard
│   ├── label_interface.html  # Labeling interface
│   ├── upload_data.html  # Data upload page
│   └── analytics.html    # Analytics dashboard
├── static/              # Static files
│   └── style.css        # Custom CSS styles
└── env/                 # Virtual environment
```

## Database Schema

The application uses SQLite with the following tables:

### crash_narratives
- `id`: Primary key
- `narrative`: Text of the crash narrative
- `severity_label`: Crash severity classification
- `category_label`: Type of crash
- `weather_condition`: Weather during crash
- `time_of_day`: Time period of crash
- `vehicle_type`: Primary vehicle involved
- `labeled_by`: Name of person who labeled
- `created_at`: When narrative was uploaded
- `labeled_at`: When narrative was labeled

### labeling_stats
- `id`: Primary key
- `total_narratives`: Total number of narratives
- `labeled_narratives`: Number of labeled narratives
- `unlabeled_narratives`: Number of unlabeled narratives
- `last_updated`: Last update timestamp

## CSV Format for Upload

Your CSV file should have the following format:

```csv
narrative,case_id
"Vehicle 1 was traveling eastbound when it collided with Vehicle 2...",CASE001
"Single vehicle rollover occurred during heavy rain conditions...",CASE002
```

**Required**: The CSV must contain a column named "narrative"
**Optional**: Additional columns are ignored during import

## API Endpoints

- `GET /`: Dashboard with statistics and recent activity
- `GET /label`: Labeling interface for next unlabeled narrative
- `POST /submit_label`: Submit labels for a narrative
- `GET /upload_data`: Data upload interface
- `POST /upload_data`: Process uploaded CSV file
- `GET /analytics`: Analytics dashboard with charts
- `GET /export_labels`: Export all labeled data as JSON

## Features in Detail

### Labeling Interface
- Clean, intuitive design with radio buttons for each category
- Progress tracking and navigation
- Validation to ensure all fields are completed
- Skip functionality for difficult cases

### Analytics Dashboard
- Interactive charts using Chart.js
- Real-time statistics updates
- Distribution analysis for all label categories
- Export functionality for further analysis

### Data Management
- SQLite database for reliable data storage
- Automatic database initialization
- Data validation and error handling
- Backup and export capabilities

## Customization

### Adding New Label Categories
1. Update the HTML templates with new radio button options
2. Modify the database schema in `app.py`
3. Update the analytics queries and charts
4. Add validation for new fields

### Styling
- Modify `static/style.css` for custom styling
- Templates use Bootstrap 5 for responsive design
- Charts powered by Chart.js for interactivity

## Troubleshooting

### Common Issues
1. **Database errors**: Delete `crash_narratives.db` and restart the app
2. **CSV upload fails**: Ensure your CSV has a "narrative" column
3. **Port conflicts**: Change the port in `app.py` line: `app.run(port=5001)`

### Getting Help
- Check the browser console for JavaScript errors
- Look at the terminal output for Python errors
- Ensure all dependencies are installed correctly

## Future Enhancements

- User authentication and role management
- Batch labeling operations
- Machine learning model integration
- Advanced search and filtering
- Label quality assessment
- Inter-annotator agreement calculations
- REST API for external integrations

## License

This project is open-source and available for educational and research purposes.

---

**Happy Labeling!** 🚗📊

For questions or issues, please check the console output and ensure all dependencies are properly installed.
