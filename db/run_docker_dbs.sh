#!/bin/bash
# Scripts to run temporary multiple mysql DBs on the localhost, under docker.

readonly num_dbs=3

start_docker_dbs() {
  for db in `seq 1 $num_dbs`; do
    sudo docker run --detach --name=mysql$db --env="MYSQL_ROOT_PASSWORD=foobarzot"  mysql
    sudo docker inspect mysql$db | grep -m 1 "\"IPAddress\":" | cut -d'"' -f 4
  done
}

clean_docker_dbs() {
  for db in `seq 1 $num_dbs`; do
    sudo docker stop mysql$db
    sudo docker rm mysql$db
  done
}
