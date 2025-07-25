import os
import sys
import subprocess
import platform
import venv

def create_venv(venv_path):
    print("Creating virtual environment...")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_path)
    print("Virtual environment created.")

def install_requirements(python_exec):
    print("Installing requirements...")
    try:
        subprocess.check_call([python_exec, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed.")
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements.")
        sys.exit(1)

def main():
    venv_path = os.path.join(".", ".venv")

    if platform.system() == "Windows":
        python_exec = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_exec = os.path.join(venv_path, "bin", "python")

    if not os.path.exists(venv_path):
        create_venv(venv_path)
        install_requirements(python_exec)

    main_file = os.path.join("app", "src", "main.py")

    try:
        subprocess.run([python_exec, "-B", main_file])
    except Exception as e:
        print(f"Failed to run the app: {e}")

if __name__ == "__main__":
    main()