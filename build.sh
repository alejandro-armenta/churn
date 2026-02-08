#!/bin/bash

#find ./Generated/ -maxdepth 1 -type f ! -name 'CreateDatabase.sql' ! -name 'CurrentDatabase.sql' -delete

python Training_Pipeline.py ./myTrain.sql ./myTest.sql ./TestChurn0

python Training_Pipeline.py ./train.sql ./test.sql ./TestChurn1

python Training_Pipeline.py ./complete.sql ./test.sql ./TestChurnComplete
