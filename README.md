# AdvancedSoftwareDevelopment
A smooth webshop to buy the things you need.

## General requirements:
- Python3
- Django: `pip install django`, if necessary 

## For OSx:
- Download Docker: https://store.docker.com/editions/community/docker-ce-desktop-mac.
- `docker-compose up web` 

## For Windows 10 (not Pro):
You will have to install Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/). 
Choose both Docker Machine and Compose for the install. We ran into some problems when not choosing to download Git, so we recommend that you also choose that. But this will uninstall your existing Git version, so you could also try to point Docker Toolbox to the right location for Git bash afterwards. If you don't have VirtualBox installed already, you will also need to choose that.

Open the Docker Quickstart Terminal, and let it do its thing. (If you didn't download Git together with Docker, you will have to point to the correct location for the Git Bash). You should get a message saying "Docker is up and running!" - now you're good to go.

Go to the location of the project (`cd C:/Users/...`). The command `docker-machine ls` should show a `default` VM created for you, with a given IP address (ex: *192.168.99.100*). Run the command `docker-machine.exe env default` and run the command that is shown (`$ eval $(...)`). Your VM should now be ready for use. 
Run the command `docker-compose up`. This will take some time. After a while, you will see the message:

`Starting development server at http://0.0.0.0:8000/`  
`web_1  | Quit the server with CONTROL-C. `
 
In your browser, go to *[VM ip address]:8000*, ex *192.168.99.100:8000*. If you don't remember the ip address, it can be found by running the command `docker-machine ip default`. You should now see the login page!
