# **Real World Project: Database Shard Github**

This project is about building an app in docker-compose that will set up a sharded database, and providing a Python script that will connect, query, and demonstrate the merged database.
A single MariaDB database ( zipcode.csv) is sharded between the two servers (master amd master2) and acts as a single database.

## **Pre-requisites**

The prerequisites for this project is to install Docker, Docker Compose, Mariadb and Virtual Machine running Ubuntu 20.04.
IP address of virtual machine is 192.168.2.7..

To install Docker use commands:

	sudo apt update
	sudo apt install apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
	sudo apt update
	sudo apt install docker-ce

Check the Docker status with command:

	sudo systemctl status docker

## **Installation**

To install Docker Compose:

	sudo apt install docker-compose

To install Mariadb:

	sudo apt install mariadb-client

## **MaxScale docker-compose setup**

 After forking Zohan/maxscale-docker I cloned maxscale-docker from my repository with command:

	git clone https://github.com/vsitum/maxscale-docker.git   


To bring the containers up, navigate to maxscale-docker/maxscale/ directory and run command:

 	docker-compose up -d

Configure docker-compose.yml with 3 services:

	master, 
	master2 and
	maxscale

## **Checking**

To make sure MariaDB MaxScale is ready accepting client connections and route queries to the backend cluster, check MaxScale status with maxctrl

	docker-compose exec maxscale maxctrl list servers
	┌────────────────┬─────────┬──────┬─────────────┬─────────────────┬───────────┐
	│ Server         │ Address │ Port │ Connections │ State           │ GTID      │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_one │ master  │ 3306 │ 0           │ Master, Running │ 0-3000-32 │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_two │ master2 │ 3306 │ 0           │ Running         │ 0-3000-31 │
	└────────────────┴─────────┴──────┴─────────────┴─────────────────┴───────────┘

The user maxuser with the password maxpwd can be used to test the cluster. Assuming the mariadb client is installed 
on the  machine :

	mysql -umaxuser -pmaxpwd -h 127.0.0.1 -P 4000
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 4
	Server version: 10.5.9-MariaDB-1:10.5.9+maria~focal-log mariadb.org binary distribution

	Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

	MariaDB [(none)]> 

	MariaDB [(none)]> show databases;

		+--------------------+
		| Database           |
		+--------------------+
		| information_schema |
		| mysql              |
		| performance_schema |
		| zipcodes_one       |
		| zipcodes_two       |
		+--------------------+
		5 rows in set (0.001 sec)

The cluster is configured to utilize automatic failover. To illustrate this you can stop the master container and watch for maxscale to failover to one of the original slaves and then show it rejoining after recovery:

	sudo docker-compose stop master
	Stopping maxscale_master_1 ... done
	docker-compose exec maxscale maxctrl list servers

	┌────────────────┬─────────┬──────┬─────────────┬─────────────────┬───────────┐
	│ Server         │ Address │ Port │ Connections │ State           │ GTID      │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_one │ master  │ 3306 │ 0           │ Down            │ 0-3000-32 │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_two │ master2 │ 3306 │ 0           │ Master, Running │ 0-3000-31 │
	└────────────────┴─────────┴──────┴─────────────┴─────────────────┴───────────┘
	
	docker-compose start master
	starting master ... done
	docker-compose exec maxscale maxctrl list servers

	┌────────────────┬─────────┬──────┬─────────────┬─────────────────┬───────────┐
	│ Server         │ Address │ Port │ Connections │ State           │ GTID      │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_one │ master  │ 3306 │ 0           │ Running         │ 0-3000-32 │
	├────────────────┼─────────┼──────┼─────────────┼─────────────────┼───────────┤
	│ zip_master_two │ master2 │ 3306 │ 0           │ Master, Running │ 0-3000-31 │
	└────────────────┴─────────┴──────┴─────────────┴─────────────────┴───────────┘


## **Running**

After running python script zipcodes.py the output is shown below:

	The last 10 rows of zipcodes_one are:
	(40843, 'STANDARD', 'HOLMES MILL', 'KY', 'PRIMARY', '36.86', '-83', 'NA-US-KY-HOLMES MILL', 'FALSE', '', '', '')
	(41425, 'STANDARD', 'EZEL', 'KY', 'PRIMARY', '37.89', '-83.44', 'NA-US-KY-EZEL', 'FALSE', '390', '801', '10204009')
	(40118, 'STANDARD', 'FAIRDALE', 'KY', 'PRIMARY', '38.11', '-85.75', 'NA-US-KY-FAIRDALE', 'FALSE', '4398', '7635', '122449930')
	(40020, 'PO BOX', 'FAIRFIELD', 'KY', 'PRIMARY', '37.93', '-85.38', 'NA-US-KY-FAIRFIELD', 'FALSE', '', '', '')
	(42221, 'PO BOX', 'FAIRVIEW', 'KY', 'PRIMARY', '36.84', '-87.31', 'NA-US-KY-FAIRVIEW', 'FALSE', '', '', '')
	(41426, 'PO BOX', 'FALCON', 'KY', 'PRIMARY', '37.78', '-83', 'NA-US-KY-FALCON', 'FALSE', '', '', '')
	(40932, 'PO BOX', 'FALL ROCK', 'KY', 'PRIMARY', '37.22', '-83.78', 'NA-US-KY-FALL ROCK', 'FALSE', '', '', '')
	(40119, 'STANDARD', 'FALLS OF ROUGH', 'KY', 'PRIMARY', '37.6', '-86.55', 'NA-US-KY-FALLS OF ROUGH', 'FALSE', '760', '1468', '20771670')
	(42039, 'STANDARD', 'FANCY FARM', 'KY', 'PRIMARY', '36.75', '-88.79', 'NA-US-KY-FANCY FARM', 'FALSE', '696', '1317', '20643485')
	(40319, 'PO BOX', 'FARMERS', 'KY', 'PRIMARY', '38.14', '-83.54', 'NA-US-KY-FARMERS', 'FALSE', '', '', '')



	The first 10 rows of zipcodes_two are:
	(42040, 'STANDARD', 'FARMINGTON', 'KY', 'PRIMARY', '36.67', '-88.53', 'NA-US-KY-FARMINGTON', 'FALSE', '465', '896', '11562973')
	(41524, 'STANDARD', 'FEDSCREEK', 'KY', 'PRIMARY', '37.4', '-82.24', 'NA-US-KY-FEDSCREEK', 'FALSE', '', '', '')
	(42533, 'STANDARD', 'FERGUSON', 'KY', 'PRIMARY', '37.06', '-84.59', 'NA-US-KY-FERGUSON', 'FALSE', '429', '761', '9555412')
	(40022, 'STANDARD', 'FINCHVILLE', 'KY', 'PRIMARY', '38.15', '-85.31', 'NA-US-KY-FINCHVILLE', 'FALSE', '437', '839', '19909942')
	(40023, 'STANDARD', 'FISHERVILLE', 'KY', 'PRIMARY', '38.16', '-85.42', 'NA-US-KY-FISHERVILLE', 'FALSE', '1884', '3733', '113020684')
	(41743, 'PO BOX', 'FISTY', 'KY', 'PRIMARY', '37.33', '-83.1', 'NA-US-KY-FISTY', 'FALSE', '', '', '')
	(41219, 'STANDARD', 'FLATGAP', 'KY', 'PRIMARY', '37.93', '-82.88', 'NA-US-KY-FLATGAP', 'FALSE', '708', '1397', 	'20395667')
	(40935, 'STANDARD', 'FLAT LICK', 'KY', 'PRIMARY', '36.82', '-83.76', 'NA-US-KY-FLAT LICK', 'FALSE', '752', '1477', '14267237')
	(40997, 'STANDARD', 'WALKER', 'KY', 'PRIMARY', '36.88', '-83.71', 'NA-US-KY-WALKER', 'FALSE', '', '', '')
	(41139, 'STANDARD', 'FLATWOODS', 'KY', 'PRIMARY', '38.51', '-82.72', 'NA-US-KY-FLATWOODS', 'FALSE', '3692', '6748', '121902277')


	The smallest zipcode number in zipcodes_two is:
	(38257,)

	The largest zipcode number in zipcodes_one is:
	(47750,)

Once complete, to remove the cluster and maxscale containers:

	docker-compose down -v

## **Sources**

	https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04 
 
	https://docs.docker.com/compose/install
  
	https://mariadb.com/kb/en/mariadb-maxscale-25-simple-sharding-with-two-servers
  
	https://www.digitalocean.com/community/tutorials/how-to-store-and-retrieve-data-in-mariadb-using-python-on-          ubuntu-18-04 
