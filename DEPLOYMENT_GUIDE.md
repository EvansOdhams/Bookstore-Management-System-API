# Deployment Guide for Bookstore Management System API

## Development vs Production

### Current Setup (Development)
- Flask development server
- Debug mode enabled
- Hardcoded API keys
- JSON file storage
- CORS enabled for all origins

### Production Considerations

⚠️ **Important**: The current setup is for development only. For production, you need to:

1. Use a production WSGI server (Gunicorn, uWSGI, Waitress)
2. Disable debug mode
3. Use environment variables for configuration
4. Implement proper database (PostgreSQL, MySQL, MongoDB)
5. Set up proper CORS policies
6. Use HTTPS
7. Implement rate limiting
8. Set up logging and monitoring
9. Use proper API key management (database or secrets manager)

## Deployment Options

### Option 1: Local/Internal Network Deployment

#### Using Waitress (Windows-friendly)

1. **Install Waitress:**
   ```bash
   pip install waitress
   ```

2. **Create production app file** (`run_production.py`):
   ```python
   from waitress import serve
   from src.api.app import create_app
   
   app = create_app()
   
   if __name__ == '__main__':
       print("Starting production server on http://0.0.0.0:5000")
       serve(app, host='0.0.0.0', port=5000, threads=4)
   ```

3. **Run:**
   ```bash
   python run_production.py
   ```

#### Using Gunicorn (Linux/Mac)

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Run:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "src.api.app:create_app()"
   ```

### Option 2: Cloud Deployment

#### A. Heroku

1. **Create `Procfile`:**
   ```
   web: gunicorn src.api.app:create_app
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11
   ```

3. **Install Heroku CLI** and deploy:
   ```bash
   heroku create bookstore-api
   git push heroku main
   ```

#### B. PythonAnywhere

1. Upload project files
2. Set up virtual environment
3. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/bookstore-api'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from src.api.app import create_app
   application = create_app()
   ```
4. Point domain to WSGI file

#### C. AWS (EC2/Elastic Beanstalk)

1. **Create `application.py`** (for Elastic Beanstalk):
   ```python
   from src.api.app import create_app
   application = create_app()
   ```

2. **Create `.ebextensions/python.config`:**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: application:application
   ```

3. Deploy using EB CLI or console

#### D. Docker Deployment

1. **Create `Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.api.app:create_app()"]
   ```

2. **Create `docker-compose.yml`:**
   ```yaml
   version: '3.8'
   services:
     api:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./data:/app/data
       environment:
         - FLASK_ENV=production
   ```

3. **Build and run:**
   ```bash
   docker build -t bookstore-api .
   docker run -p 5000:5000 bookstore-api
   ```

### Option 3: Windows Service (For Windows Server)

1. **Install NSSM** (Non-Sucking Service Manager)
2. **Create service:**
   ```bash
   nssm install BookstoreAPI "C:\Python311\python.exe" "D:\path\to\run_production.py"
   ```
3. **Start service:**
   ```bash
   nssm start BookstoreAPI
   ```

## Production Configuration

### Environment Variables

Create `.env` file (and add to `.gitignore`):

```env
FLASK_ENV=production
FLASK_DEBUG=False
API_KEYS=your-secure-api-key-1,your-secure-api-key-2
DATABASE_URL=sqlite:///data/bookstore.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
```

### Update `src/api/app.py` for Production

```python
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Production settings
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # ... rest of the code
```

### Update Authentication

Replace hardcoded API keys with environment variables:

```python
# In src/api/auth.py
import os

VALID_API_KEYS = {
    key.strip(): 'user' 
    for key in os.getenv('API_KEYS', 'test-api-key-123').split(',')
}
```

## Security Checklist

- [ ] Disable debug mode
- [ ] Use environment variables for secrets
- [ ] Implement HTTPS/SSL
- [ ] Set up proper CORS policies
- [ ] Add rate limiting
- [ ] Implement request logging
- [ ] Use secure API key storage
- [ ] Add input validation and sanitization
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Regular security updates

## Monitoring and Logging

### Add Logging

```python
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)
    
    # Logging setup
    if not app.debug:
        file_handler = RotatingFileHandler('logs/bookstore.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Bookstore API startup')
    
    # ... rest of code
```

## Database Migration (Future Enhancement)

For production, consider migrating from JSON files to a database:

1. **SQLite** (simple, file-based)
2. **PostgreSQL** (robust, production-ready)
3. **MongoDB** (NoSQL, document-based)

Example with SQLAlchemy:
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)
    # ... rest of code
```

## Testing Before Deployment

1. **Run all tests:**
   ```bash
   pytest tests/ -v
   ```

2. **Load testing** (using Apache Bench or Locust):
   ```bash
   ab -n 1000 -c 10 -H "X-API-Key: test-api-key-123" http://localhost:5000/api/inventory/books
   ```

3. **Security testing:**
   - Test without API key
   - Test with invalid API key
   - Test SQL injection (if using database)
   - Test XSS vulnerabilities

## Quick Production Setup Script

Create `setup_production.py`:

```python
import os
import shutil

# Create necessary directories
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Copy .env.example to .env if it doesn't exist
if not os.path.exists('.env'):
    shutil.copy('.env.example', '.env')
    print("Created .env file. Please update it with your configuration.")

print("Production setup complete!")
```

## Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Debug mode disabled
- [ ] Production WSGI server configured
- [ ] HTTPS/SSL certificate installed
- [ ] CORS policies set
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated

## Support

For issues or questions:
1. Check logs: `logs/bookstore.log`
2. Review error messages
3. Check API documentation: `/apidocs`
4. Verify environment variables
5. Test endpoints individually

