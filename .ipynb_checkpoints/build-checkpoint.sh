#!/bin/bash

#find ./Generated/ -maxdepth 1 -type f ! -name 'original.csv' -delete
find ./Generated/ -maxdepth 1 -type f -delete

python Training_Pipeline.py
