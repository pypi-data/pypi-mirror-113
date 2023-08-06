# 3DN Python SDK

## Setup Symbolic Links

### Windows

This repository uses symbolic links. Please enable support for it on your Windows setup, before cloning this repository.

1. Enable symlinks in Git: `git config --global core.symlinks true`
2. Enable symlink policy:
    1. Run `gpedit.msc`
    2. Computer configuration → Windows Settings → Security Settings → Local Policies → User Rights Assignment
    3. Edit `Create symbolic links` policy and add your Windows user to it
    4. Save and reboot

## Setup Visual Studio Code

### Open VSC environment

**Note:** The `vscode` script works with the non-portable version of VSC only. And VSC needs to be in the path.

```sh
./vscode .
```

### Setup VSC environment

```sh
# Install VSC extensions
./vscode --install-extension editorconfig.editorconfig
./vscode --install-extension ms-python.python
./vscode --install-extension esbenp.prettier-vscode

# Open VSC environment
./vscode .

# Install IDE tools
python3 -m venv ./envs/ide
source ./envs/ide/bin/activate   # Bash & co
./envs/ide/Scripts/activate.bat  # Powershell
python3 -m pip install yapf
python3 -m pip install pylint
```

Open a Python file and select the previously created `ide` Python virtual environment in the status bar of VSC.

## Setup Python Interpreter

### Python 2.7 on Ubuntu 20.04 LTS

```sh
# install python 2.7
sudo apt install python2
# install pip for python 2.7
sudo apt install curl
curl https://bootstrap.pypa.io/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
# validate versions
python2 --version
pip --version
# configure virtual environment
sudo pip install virtualenv
virtualenv -p /bin/python2 ./envs/py2
source ./envs/py2/bin/activate
```

## Setup Mockoon Server

1. Install Mockoon: `npm install -g @mockoon/cli`
2. Start the mock server: `mockoon-cli start --data api/mock/mockoon.json -i 0`
3. List running mock servers: `mockoon-cli list`
4. Stop the mock servers: `mockoon-cli stop`

## Setup Virtual Environment

### Python 3.x

1. Setup a new environment: `python3 -m venv ./envs/py3` (make sure to run python 3.x)
2. Activate environment: `source ./envs/py3/bin/activate` on Unix and `source ./envs/py3/Scripts/activate` (Bash) or `envs\py3\Scripts\activate.bat` (Cmd/PowerShell) on Windows
3. Update pip: `python -m pip install --upgrade pip`
4. Install core library: `pip install -e sdk/core`
5. Install ui library: `pip install -e sdk/blender` (make sure to run it AFTER core)
6. Deactivate the environment: `deactivate`

### Python 2.7

1. Setup a new environment: `pip install virtualenv && virtualenv -p /usr/bin/python ./envs/py2` (make sure the path is pointing to Python 2.7 on your system)
2. Activate environment: `source ./envs/py2/bin/activate` on Unix and `source ./envs/py2/Scripts/activate` (Bash) or `envs\py2\Scripts\activate.bat` (Cmd/PowerShell) on Windows
3. Update pip: `python -m pip install --upgrade pip`
4. Install core library: `pip install -e sdk/core`
5. Install ui library: `pip install -e sdk/blender` (make sure to run it AFTER core)
6. Deactivate the environment: `deactivate`
