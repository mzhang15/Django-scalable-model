sudo apt-get install libssl-dev

setup database locally:

systemctl service mysql start // start a mysql server
systemctl status mysql.service // check if the server is running

sudo mysql -u root -p // login to mysql as root user

show databases; // show available databases on mysql

create database default_db // create database default_db as our default database
create database db1;
create database db2;

// create appserver user for mysql and give it access to all 3 databases
create user appserver identified by '1234';
grant all on default_db.* to 'appserver'@'localhost';
flush privileges;
grant all on db1.* to 'appserver'@'localhost';
flush privileges;
grant all on db2.* to 'appserver'@'localhost';
flush privileges;

control + D // logout database

mysql -u appserver -p //log into database as appserver
show databases // you should see all 3 databases we created

python manage.py makemigrations demo scalable
python manage.py migrate --database=default
python manage.py migrate --database=db1
python manage.py migrate --database=db2

// now you can test save() and router by writing testcase or run shell
python manage.py shell // start shell

// in the shell do following
from demo.models import user
u = User(name=<value>)
u.save()
