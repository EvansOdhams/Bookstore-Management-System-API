# Production Server Setup Guide

## Quick Start: Switch to Production Server

### Step 1: Stop the Development Server

If your development server is running, press `CTRL+C` to stop it.

### Step 2: Start Production Server

Simply run:
```bash
python run_production.py
```

That's it! The server will now run using **Waitress**, a production-ready WSGI server.

## Differences: Development vs Production

### Development Server (`python src/api/app.py`)
- ❌ Flask development server (not for production)
- ✅ Debug mode ON (auto-reload on code changes)
- ✅ Detailed error pages
- ⚠️ Single-threaded
- ⚠️ Not optimized for production

### Production Server (`python run_production.py`)
- ✅ Waitress WSGI server (production-ready)
- ✅ Debug mode OFF (secure)
- ✅ Multi-threaded (4 worker threads)
- ✅ Optimized for production use
- ✅ No auto-reload (better performance)

## Server Comparison

| Feature | Development | Production (Waitress) |
|---------|------------|----------------------|
| Server Type | Flask Dev Server | Waitress WSGI |
| Debug Mode | ON | OFF |
| Auto-reload | Yes | No |
| Threads | 1 | 4 |
| Performance | Low | High |
| Security | Lower | Higher |
| Production Ready | ❌ No | ✅ Yes |

## Running the Production Server

### Basic Usage
```bash
python run_production.py
```

### Custom Port
Edit `run_production.py` and change:
```python
serve(app, host='0.0.0.0', port=8080, threads=4)  # Change port to 8080
```

### More Threads (for higher traffic)
```python
serve(app, host='0.0.0.0', port=5000, threads=8)  # 8 worker threads
```

## Verifying Production Mode

1. **Check the startup message:**
   - Should say "Mode: Production (Debug: OFF)"
   - Should say "Server: Waitress WSGI Server"

2. **Test an endpoint:**
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:5000/health" -Headers @{"X-API-Key"="test-api-key-123"}
   ```

3. **Check for debug mode:**
   - If you get an error, it should NOT show detailed stack traces
   - Error pages should be generic (not showing code)

## Performance Tuning

### Adjust Thread Count

For **low traffic** (testing, small team):
```python
serve(app, host='0.0.0.0', port=5000, threads=2)
```

For **moderate traffic** (default):
```python
serve(app, host='0.0.0.0', port=5000, threads=4)
```

For **high traffic**:
```python
serve(app, host='0.0.0.0', port=5000, threads=8)
```

### Connection Limits

Add connection limits for better resource management:
```python
serve(
    app, 
    host='0.0.0.0', 
    port=5000, 
    threads=4,
    channel_timeout=120,  # Timeout in seconds
    cleanup_interval=30    # Cleanup interval
)
```

## Running as a Windows Service

### Option 1: Using NSSM (Recommended)

1. **Download NSSM**: https://nssm.cc/download
2. **Install service:**
   ```cmd
   nssm install BookstoreAPI "C:\Python311\python.exe" "D:\path\to\run_production.py"
   ```
3. **Start service:**
   ```cmd
   nssm start BookstoreAPI
   ```

### Option 2: Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `run_production.py`
   - Start in: Your project directory

## Monitoring Production Server

### Check if Server is Running
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000
```

### View Logs
The server output will show:
- Request logs
- Error messages
- Access patterns

### Health Monitoring
Set up a monitoring script to check `/health` endpoint regularly.

## Troubleshooting

### Port Already in Use
```python
# Change port in run_production.py
serve(app, host='0.0.0.0', port=8080, threads=4)
```

### Server Not Starting
1. Check if Python path is correct
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check for errors in the console output

### Performance Issues
1. Increase thread count
2. Check system resources (CPU, memory)
3. Consider using a reverse proxy (nginx) for static files

## Next Steps for Production Deployment

1. ✅ **Use Production Server** (You're here!)
2. **Set up environment variables** for configuration
3. **Use HTTPS** with SSL certificate
4. **Set up reverse proxy** (nginx, Apache)
5. **Implement logging** to files
6. **Set up monitoring** (Sentry, New Relic)
7. **Configure backups** for data files
8. **Set up CI/CD** pipeline

## Quick Reference

**Development:**
```bash
python src/api/app.py
```

**Production:**
```bash
python run_production.py
```

**Stop Server:**
Press `CTRL+C`

**Test Server:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

