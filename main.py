import os 
from os.path import join
from sql_parser import analyze_lines
from comment import comment_filter

for root, dirs, files in os.walk("E:\study\Coding\Python\SQL_depend_analyser\sql"):
    for each_file in files:
        f = open(join(each_file), 'r')
        lines = comment_filter(f.read())
        analyzed = analyze_lines(lines)
        print each_file
        analyzed.demo()
        print ''
    
