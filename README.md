# MovieLunch.ru Admin Panel and Website

This repository contains the complete codebase for the MovieLunch.ru website and its admin panel. The admin panel allows for easy management of the website content and task tracking.

## Project Structure

- `/admin` - Flask-based admin panel application
- `/website` - Main public website files
- `/docs` - Documentation and user guides

## Features

### Admin Panel
- User authentication with JWT
- Task management system
- Content editing capabilities
- Real-time synchronization with the main website

### Website
- Responsive design for all devices
- Task progress tracking
- Detailed analysis and recommendations

## Installation

### Prerequisites
- Python 3.8+
- MySQL database
- Node.js (for frontend development)

### Setup Admin Panel

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the database:
```bash
# Edit the database connection in admin/main.py if needed
```

4. Run the application:
```bash
python -m admin.main
```

5. Access the admin panel at http://localhost:5000

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

**Important:** Change the default password after the first login.

## Usage

Detailed usage instructions are available in the [Admin Panel Manual](docs/manual.html).

## Development

### Admin Panel
The admin panel is built with Flask and uses:
- Flask-SQLAlchemy for database operations
- PyJWT for authentication
- RESTful API architecture

### Website
The website is built with:
- HTML5, CSS3, and JavaScript
- Responsive design principles
- Modern UI/UX practices

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please contact STORYART - Digital Studio.
