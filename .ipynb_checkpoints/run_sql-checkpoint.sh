#!/bin/bash
echo "Alejandro"

sudo -u alejandro psql -d churn -f average.sql

#"set search_path to socialnet7;show search_path;select * from event;"