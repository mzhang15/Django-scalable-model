#!/bin/bash

sql_file=scalica.sql

set -x

if [ $# -gt 0 ]; then
  case $1 in
    "remove")
      sql_file=remove_scalica.sql
      ;;
    *)
      echo "unknown command: $1"
      exit 1
  esac
fi

for db in `seq 2 4`; do
  mysql -u root -p -h 172.17.0.$db < ${sql_file}
done
