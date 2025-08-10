#!/usr/bin/env python3
"""
Startup check script for Railway deployment
"""
import os
import sys

def check_environment():
    """Check if all required environment variables are set."""
    print("=== RAILWAY STARTUP CHECK ===")
    
    # Check critical environment variables
    critical_vars = ['PORT', 'DATABASE_URL']
    optional_vars = ['SECRET_KEY', 'OPENAI_API_KEY', 'DEBUG']
    
    print("\n--- Critical Variables ---")
    for var in critical_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("\n--- Optional Variables ---")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: NOT SET (optional)")
    
    print("\n--- System Info ---")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    # Check if Django files exist
    django_files = ['manage.py', 'CVProject/settings.py', 'requirements.txt']
    print("\n--- Django Files Check ---")
    for file in django_files:
        if os.path.exists(file):
            print(f"✅ {file}: EXISTS")
        else:
            print(f"❌ {file}: MISSING")
    
    print("\n=== END STARTUP CHECK ===")

if __name__ == "__main__":
    check_environment()
