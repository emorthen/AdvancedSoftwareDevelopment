# AdvancedSoftwareDevelopment Group 9

A smooth webshop to buy and sell rockets. To the moon!
The database is local, so you have to add products that will be displayed in the webshop. This can be done on localhost:8000/admin (log in with the superuser you created in the terminal as discribed below).

## General requirements:

* Python 3
* Docker

## For OSx:

* Download Docker: https://store.docker.com/editions/community/docker-ce-desktop-mac.
* Run Docker
* From root of project:  
  -- `./setup`  
  -- `docker-compose up web`
* Run in web browser on localhost:8000

## For Windows 10 (not Pro):

* Install Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/).
  * Choose both Docker Machine and Compose for the install. We ran into some problems when not choosing to download Git, so we recommend that you also choose that. But this will uninstall your existing Git version, so you could also try to point Docker Toolbox to the right location for Git bash afterwards.
  * If you don't have VirtualBox installed already, you will also need to choose that.
* Open the Docker Quickstart Terminal, and let it do its thing. (If you didn't download Git together with Docker, you will have to point to the correct location for the Git Bash).
  * You should get a message saying "Docker is up and running!".
* From root of project:
  * `pip install django`
  * `pip install django-cart`
  * `python manage.py makemigrations cart`
  * `python manage.py migrate cart`
  * `python manage.py makemigrations webshop`
  * `python manage.py migrate webshop`
  * `python manage.py createsuperuser`, to add admin users for /admin
* Set up the VM
  * From root of project the command `docker-machine ls` should show a `default` VM created for you, with a given IP address (ex: _192.168.99.100_).
  * From root of project run the command `docker-machine.exe env default` and run the command that is shown (`$ eval $(...)`). Your VM should now be ready for use.
* From root of project run `docker-compose up`. This will take some time. After a while, you should see the message:
  `Starting development server at http://0.0.0.0:8000/`  
  `web_1 | Quit the server with CONTROL-C.`
  * If no message appears, try to access the web page and see if it still works.
  * If not, try creating a new VM (ex: tdt4242) from root of project
    * `docker-machine create tdt4242`
    * `docker-machine.exe env tdt4242`
    * `$ eval $(...)`
* In your browser, go to _[VM ip address]:8000_, ex _192.168.99.100:8000_. If you don't remember the ip address, it can be found by running the command `docker-machine ip nameOfVM`. You should now see the login page!
