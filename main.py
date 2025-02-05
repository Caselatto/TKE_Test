import os
import subprocess
import sys

def run_tests():
    print("Activating virtual environment...")
    venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "activate")

    print("Running BDD tests...")
    os.system(f'cmd /c "{venv_path} && python -m behave --format=json --outfile=test_report.json"')

if __name__ == "__main__":
    run_tests()
