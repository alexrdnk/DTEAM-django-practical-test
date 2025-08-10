#!/usr/bin/env python3
"""
Django debug script for Railway deployment
"""
import os
import sys

def test_django_step_by_step():
    """Test Django step by step to identify the exact failure point."""
    print("=== DJANGO DEBUG TEST ===")
    
    try:
        # Step 1: Add project to Python path
        project_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_dir)
        print("✅ Step 1: Project directory added to Python path")
        
        # Step 2: Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings')
        print("✅ Step 2: DJANGO_SETTINGS_MODULE set")
        
        # Step 3: Try to import Django
        try:
            import django
            print(f"✅ Step 3: Django imported successfully: {django.get_version()}")
        except Exception as e:
            print(f"❌ Step 3: Django import failed: {e}")
            return False
        
        # Step 4: Try to setup Django
        try:
            django.setup()
            print("✅ Step 4: Django setup completed")
        except Exception as e:
            print(f"❌ Step 4: Django setup failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 5: Try to import settings
        try:
            from django.conf import settings
            print("✅ Step 5: Django settings imported")
        except Exception as e:
            print(f"❌ Step 5: Django settings import failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 6: Try to import database
        try:
            from django.db import connection
            print("✅ Step 6: Django database imported")
        except Exception as e:
            print(f"❌ Step 6: Django database import failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 7: Try to test database connection
        try:
            connection.ensure_connection()
            print("✅ Step 7: Database connection test successful")
        except Exception as e:
            print(f"❌ Step 7: Database connection test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("=== DJANGO DEBUG TEST COMPLETED SUCCESSFULLY ===")
        return True
        
    except Exception as e:
        print(f"❌ Django debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_django_step_by_step()
