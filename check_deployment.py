#!/usr/bin/env python3
"""
Quick check to verify deployment readiness
"""
import os

def check_structure():
    print("🔍 Checking project structure...")
    
    structure = {
        'app.py': 'Main application',
        'requirements.txt': 'Python dependencies',
        'vercel.json': 'Vercel configuration',
        'templates/index.html': 'HTML template',
        'static/css/main.css': 'Main styles',
        'static/css/components.css': 'Component styles',
        'static/js/ui.js': 'UI JavaScript',
        'static/js/main.js': 'Main JavaScript',
        'converter/__init__.py': 'Converter package',
        'converter/pure_python_converter.py': 'Pure Python converter',
        'converter/coordinate_utils.py': 'Coordinate utilities'
    }
    
    all_good = True
    for file_path, description in structure.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def check_requirements():
    print("\n🔍 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            print("✅ requirements.txt content:")
            print(content)
            return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Ghana Coordinate Converter - Deployment Check")
    print("=" * 50)
    
    structure_ok = check_structure()
    requirements_ok = check_requirements()
    
    print("\n" + "=" * 50)
    if structure_ok and requirements_ok:
        print("✅ ALL CHECKS PASSED - Ready for deployment!")
    else:
        print("❌ DEPLOYMENT CHECKS FAILED - Please fix issues above")