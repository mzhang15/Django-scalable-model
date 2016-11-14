First installation:

Install required packages.
$ sudo apt-get update; sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv
(Set a mysql root password)

$ ./first_install.sh

Install the proper databases
$ cd db
$ source ./run_docker_dbs.sh
$ start_docker_dbs
$ ./install_db.sh
(Will ask for the mysql root password configured above).
$ cd ..

Sync the database
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py makemigrations micro
$ python manage.py migrate --database auth_db
$ python manage.py migrate --database db1
$ python manage.py migrate --database db2


# After the first installation, from the project's directory
Run the server:
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py runserver

Access the site at http://localhost:8000/micro
