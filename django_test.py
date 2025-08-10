#!/usr/bin/env python3
"""
Django import test for Railway deployment
"""
import os
import sys
import django

def test_django_import():
    """Test if Django can be imported and configured properly."""
    print("=== DJANGO IMPORT TEST ===")
    
    try:
        # Add the project directory to Python path
        project_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_dir)
        
        print("✅ Project directory added to Python path")
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings')
        print("✅ DJANGO_SETTINGS_MODULE set to CVProject.settings")
        
        # Try to import Django
        import django
        print(f"✅ Django imported successfully: {django.get_version()}")
        
        # Try to configure Django
        django.setup()
        print("✅ Django setup completed successfully")
        
        # Try to import some Django modules
        from django.conf import settings
        print("✅ Django settings imported successfully")
        
        print("=== DJANGO IMPORT TEST COMPLETED ===")
        return True
        
    except Exception as e:
        print(f"❌ Django import test failed: {e}")
        import traceback
        traceback.print_exc()
        print("=== DJANGO IMPORT TEST FAILED BUT CONTINUING ===")
        return False

if __name__ == "__main__":
    test_django_import()
