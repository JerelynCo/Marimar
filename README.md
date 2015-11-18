# Open Data PH Hackathon Vagrant Box
- - -
## What's Inside
### Ubuntu 14.04 - Trusty Tahr
1. Anaconda Python 3.5 and all default Anaconda modules
    - Flask-RESTful
        - Useful for quickly creating web APIs
    - Geocoder
        - Quick Geocode and boundary lookups
    - PyMongo
        - For MongoDB interaction
2. Default MySQL Installation
3. Default MongoDB Installation
4. NodeJS
    - Includes bower and grunt default installation
    - Also has Bootstrap via Bower

## Installation
1. Install VirtualBox and Vagrant.
2. Clone this repo.
3. Download  [this file] (https://drive.google.com/file/d/0Byl_qxkqW6EWOGM0NUh2OEM1V1E/view?usp=sharing) and place it in the cloned folder.  
4. Run
```sh
vagrant box add hackathon hackathon.box
vagrant up
vagrant ssh
```
5. Set up your git config inside the VM
```sh
git config --global user.name <username>
git config --global user.email <email@email>
```
6. To logout of the SSH session, just ctrl-C or close close the terminal.
7. To shutdown the VM, go to the cloned folder and type in the ff:
```sh
vagrant halt
```

## Usage
### Accessing shared files and folders
- Root directory in Host Machine (where the Vagrantfile resides) is the main shared folder.
- Using the VM to access the shared files:
```sh
    cd /vagrant
```

### Running an HTTP server
```sh
cd <dir>
python -m http.server
```
###### Go to localhost:8000 on your browser

### PyCharm/IDE Python Connection
- Just SSH into the local port 2222 and you're good to go!

### MongoDB
- Connect via the local port 27017

### MySQL
- Username: root
- Password: toor
- Port: 3306

- - -
>"Don't worry about what anybody else is going to do. The best way to predict the future is to invent it."
-Alan Kay
