# Logs Zipper

Program written in Python 3.7 that lets you zip logs files according to their creation time.

#### Running Instructions
In order to run this program you need to provide three arguments:
    
input_dir - a directory containing the logs files  
output_dir - a directory to which the zip files will be written  
workers - a number of workers to run the search process and zip process

E.g
```
python main.py ./test/input/ ./test/output/ 3
```

* if you are to use this run command, make sure to first create the output directory in the test directory
