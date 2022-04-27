## Group Members - Group 12
* Brian Dietrick     - dietrickb20@students.ecu.edu
* Bhargavi Sanikommu - sanikommub19@students.ecu.edu
* Emily Morales      - moralesem18@students.ecu.edu

## Video Link
https://ecu.instructuremedia.com/embed/059727c0-0e11-46a7-b526-5b3c8e33d286

## Quick Start
### Local Test Setup
First, we need to install a Python 3 virtual environment with:
```
sudo apt update
sudo apt-get install python3-venv
```

Create a virtual environment:
```
python3 -m venv python_venv
```

You need to activate the virtual environment when you want to use it:
```
source python_venv/bin/activate
```

To fufil all the requirements for the python server, you need to run:
```
pip3 install -r requirements.txt
```
Because we are now inside a virtual environment. We do not need sudo.

Then you can start the server with:
```
python3 app.py
```