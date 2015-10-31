import os 
from os.path import join
from sql_parser import analyze_file
from comment import comment_filter

for root, dirs, files in os.walk("E:\study\Coding\Python\SQL_depend_analyser\sql"):
    for each_file in files:
        f = open(join(root, each_file), 'r')
        analyze_file(f).demo()
    
