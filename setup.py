import os
import subprocess
import venv
import pip


def create_venv():
    if not os.path.isdir(".venv"):
        # venv.create(".")
        venv.EnvBuilder(with_pip=True).create(".venv")


def install_requirements():
    pip_executable = os.path.join(".venv", 'Scripts', 'pip') if os.name == 'nt' else os.path.join(".venv", 'bin', 'pip')
    subprocess.run([pip_executable, "install", "-r", "requirements.txt"])
    if hasattr(pip, 'main'):
        pip.main(['install', "-r", "requirements.txt"])
    else:
        pip._internal.main(['install', "-r", "requirements.txt"])


def activate_venv():
    if os.name == "nt":  # Windows
        subprocess.run([os.path.join(".venv", "Scripts", "activate.bat")])
    else:  # Linux/macOS
        subprocess.run([os.path.join(".venv", "bin", "activate")])


def get_repo():
    subprocess.run(["git clone https://github.com/yardenmizrahi/ErgoAI"], shell=True)
    subprocess.run(["git clone https://github.com/0ded/Sitting-Posture-Recognition ErgoAI\\Posture\\Sitting-Posture-Recognition"],
                   shell=True)


def main():
    # Create the virtual environment
    create_venv()

    get_repo()

    # Activate the virtual environment
    activate_venv()

    # Install dependencies
    install_requirements()


if __name__ == "__main__":
    main()
