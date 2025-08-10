#!/usr/bin/env python3
"""
Comprehensive Railway startup script with error handling
"""
import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors gracefully."""
    print(f"\n=== {description} ===")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (return code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Main startup process."""
    print("=== RAILWAY STARTUP PROCESS ===")
    
    # Step 1: Environment check
    print("\n--- Environment Check ---")
    print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
    print(f"DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    print(f"SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Step 2: Startup check
    if not run_command("python startup_check.py", "Startup Check"):
        print("⚠️ Startup check failed, but continuing...")
    
    # Step 3: Django check
    if not run_command("python manage.py check", "Django Check"):
        print("❌ Django check failed - stopping startup")
        sys.exit(1)
    
    # Step 4: Database test (skip if it fails)
    if not run_command("python manage.py dbshell -c 'SELECT 1;'", "Database Test"):
        print("⚠️ Database test failed, but continuing...")
    
    # Step 5: Migrations
    if not run_command("python manage.py migrate --noinput", "Migrations"):
        print("❌ Migrations failed - stopping startup")
        sys.exit(1)
    
    # Step 6: Collect static
    if not run_command("python manage.py collectstatic --noinput", "Collect Static"):
        print("⚠️ Collect static failed, but continuing...")
    
    # Step 7: Start Gunicorn
    print("\n=== STARTING GUNICORN ===")
    port = os.environ.get('PORT', '8000')
    gunicorn_cmd = f"gunicorn CVProject.wsgi:application --bind 0.0.0.0:{port} --workers 1 --timeout 120 --log-level info"
    
    print(f"Starting Gunicorn on port {port}")
    print(f"Command: {gunicorn_cmd}")
    
    # Start Gunicorn (this should keep running)
    try:
        subprocess.run(gunicorn_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Gunicorn failed to start: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Gunicorn stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
