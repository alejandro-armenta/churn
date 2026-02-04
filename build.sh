#!/bin/bash

#find ./Generated/ -maxdepth 1 -type f ! -name 'CreateDatabase.sql' ! -name 'CurrentDatabase.sql' -delete

python Training_Pipeline.py ./CreateDatabase.sql ./CurrentDatabase.sql ./MyDatasetIMade

#python Training_Pipeline.py ./Generated/CreateDatabase.sql ./Generated/CurrentDatabase.sql
