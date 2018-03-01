# AdvancedSoftwareDevelopment
A smooth webshop to buy and sell rockets. To the moon!

## General requirements:
- Python3

## For OSx:
- Download Docker: https://store.docker.com/editions/community/docker-ce-desktop-mac.
- Run Docker
- From root of project:  
-- `pip3 install django`  
-- `pip3 install django-cart`  
-- `python3 manage.py migrate --run-syncdb`  
-- `python3 manage.py migrate`  
-- `python3 manage.py makemigrations cart`  
-- `python3 manage.py migrate cart`  
-- `docker-compose up`  
- Run in web browser on localhost:8000

## For Windows 10 (not Pro):
* Install Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/). 
  * Choose both Docker Machine and Compose for the install. We ran into some problems when not choosing to download Git, so we recommend that you also choose that. But this will uninstall your existing Git version, so you could also try to point Docker Toolbox to the right location for Git bash afterwards. 
  * If you don't have VirtualBox installed already, you will also need to choose that.
* Open the Docker Quickstart Terminal, and let it do its thing. (If you didn't download Git together with Docker, you will have to point to the correct location for the Git Bash). 
  * You should get a message saying "Docker is up and running!".
* Install Django from root of project: `pip install django`
* Set up the VM
  * From root of project the command `docker-machine ls` should show a `default` VM created for you, with a given IP address (ex: *192.168.99.100*). 
  * From root of project run the command `docker-machine.exe env default` and run the command that is shown (`$ eval $(...)`). Your VM should now be ready for use.
* From root of project run `docker-compose up`. This will take some time. After a while, you should see the message:
`Starting development server at http://0.0.0.0:8000/`  
`web_1  | Quit the server with CONTROL-C. `
  * If you do not get this message, try creating a new VM (ex: tdt4242) from root of project
    * `docker-machine create tdt4242` 
    * `docker-machine.exe env tdt4242`
    * `$ eval $(...)`
* In your browser, go to *[VM ip address]:8000*, ex *192.168.99.100:8000*. If you don't remember the ip address, it can be found by running the command `docker-machine ip nameOfVM`. You should now see the login page!
