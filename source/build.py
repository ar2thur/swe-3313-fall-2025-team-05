"""
This file is used to build the venv, install dependences,
and intialize the database
"""
import os
import subprocess
import venv
from pathlib import Path


def run(cmd, env=None):
    """Cleanly outputs commads to terminal and runs them"""
    print(f"\n[+] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, env=env)


def create_venv(venv_path):
    if not venv_path.exists():
        print("[+] Creating virtual environment")
        venv.EnvBuilder(with_pip=True).create(venv_path)
    else:
        print("[i] Vitrual environment already exists")


def get_venv_bins(venv_path):
    if os.name == "nt":  # Windows
        python = venv_path / "Scripts" / "python.exe"
        pip = venv_path / "Scripts" / "pip.exe"
        flask = venv_path / "Scripts" / "flask.exe"
    else:  # Mac & Linux
        python = venv_path / "bin" / "python"
        pip = venv_path / "bin" / "pip"
        flask = venv_path / "bin" / "flask"
    return python, pip, flask


def install_requirements(pip, requirements_file="requirements.txt"):
    if not Path(requirements_file).exists():
        print("[-] no requirements.txt found, skipping install.")
        return
    run([str(pip), "install", "-r", requirements_file])


def seed_database(flask):
    if not Path("webapp/db.py").exists():
        print("[-] could not find db.py, skipping database intialization.")
        return
    run([str(flask), "--app", "webapp", "reset-db"])


def main():
    project_root = Path(__file__).parent
    venv_path = project_root / "venv"

    create_venv(venv_path)

    python, pip, flask = get_venv_bins(venv_path)

    install_requirements(pip)

    seed_database(flask)

    print("[+] Set up finished")


if __name__ == "__main__":
    main()
