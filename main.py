"""
Script run all generate files in the correct order
"""
import subprocess
import sys

def run_script(script_name):
    """Run a Python script and check the result"""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print('='*60)
    
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    if result.returncode != 0:
        print(f"\nError occurred in {script_name}!")
        return False
    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║       KTPM - GENERATE ALL TEST DATA FOR ORANGEHRM        ║
╠══════════════════════════════════════════════════════════╣
║  Run order:                                              ║
║  1. generate_dim.py           (Employees, Users)         ║
║  2. generate_hr_admin.py      (HR Admin data)            ║
║  3. generate_reporting.py     (Reporting & Analytics)    ║
║  4. generate_ess.py           (Employee Self-Service)    ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    scripts = [
        'generate_dim.py',           # Must run first - create employees
        'generate_hr_admin.py',      # Need emp_number
        'generate_reporting.py',     # Reporting & Analytics
        'generate_ess.py',           # ESS (try to insert or export file)
    ]
    
    success_count = 0
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"\nStopping due to error in {script}")
            break
    
    print(f"\n{'='*60}")
    print(f"RESULT: {success_count}/{len(scripts)} scripts ran successfully")
    print('='*60)
    
    if success_count == len(scripts):
        print("""Congratulations! All data generation scripts completed successfully.""")

if __name__ == "__main__":
    main()
