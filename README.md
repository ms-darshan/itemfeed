# ITEMFEED #

Feed Generation of the Item and Variant attributes changes.
Version - 0.0.1

## Setup ##

### Fork this Repo into your account ###


### Install Python. Version >= 3.7.1 ###

### Of course replace 3.7.1 with your python version in the command below ###

```
sudo apt-get install python3.7.1-venv
```

### Create a container folder somewhere in your disk. Lets say ###

```
mkdir -p /var/www/feed
```

### Create a virtual envrironment and activate it ###

```
cd /var/www/feed && python3.7.1 -m venv env && source env/bin/activate
```
### Clone the forked repository in current directory. ###


### Install the repo's requirements.txt ###

```
cd /var/www/feed/repo-name && source ../env/bin/activate && pip install -r requirements.txt
```
### Run Item Feed ###

```
cd /var/www/htb/repo-name && source ../env/bin/activate && python server.py
```


```
	ARCHITECTURE DESIGN IS PLACED IN IMAGE FOLDER.
```
## Enjoy ##
