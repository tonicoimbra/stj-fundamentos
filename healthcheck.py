#!/usr/bin/env python
"""
Health check script for Docker containers
Returns exit code 0 if healthy, 1 if unhealthy
"""
import os
import sys

def check_database():
    """Check if database connection is working"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def check_application():
    """Check if Django application is responding"""
    try:
        import requests
        response = requests.get('http://localhost:8000/api/fundamentos/', timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Application check failed: {e}")
        return False

def main():
    """Run all health checks"""
    checks = [
        ("Database", check_database),
        ("Application", check_application),
    ]

    all_healthy = True
    for name, check_func in checks:
        if check_func():
            print(f"✅ {name}: OK")
        else:
            print(f"❌ {name}: FAILED")
            all_healthy = False

    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()
