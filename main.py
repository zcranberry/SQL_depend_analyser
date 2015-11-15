import os 
from os.path import join
from sql_parser import analyze_file
from comment import comment_filter
from config_xls_rd import *


data = xlrd.open_workbook('.\input\RDM_AFTER_20151324.xls', encoding_override = 'cp1252')
names = data.sheet_names()
table = data.sheets()[2] #Job Sheet

jobs = job_collection()
sql_name_dict = set()


for i in xrange(1, table.nrows - 1):
    #jobs.append(job(table.row_values(i)))
    j = job(table.row_values(i))
    jobs.add(j.job_name, j)
    sql_name_dict.add(j.job_name)

#for each in sql_name_dict:
#    print each
#print sql_name_dict

#count = 0
#for each_job in jobs.job_set.values():
#    if each_job.consistency_check() != True :
#        print count
#        print each_job
#        print ''
#        count += 1

file_dict = dict()

for root, dirs, files in os.walk(".\sql"):
    for each_file in files:
        #file_set.add(each_file)
        #name_stripped_extend_name = unicode(each_file.split('.')[0])
        #if name_stripped_extend_name not in sql_name_dict:
        #    print root, name_stripped_extend_name
        f = open(join(root, each_file), 'r')
        analyzed_file = analyze_file(f)
        f.close()
        file_dict[analyzed_file.job_name] = analyzed_file
        if analyzed_file.job_name not in sql_name_dict:
            print analyzed_file.job_name


wrong_set = set()

#for each in sql_name_dict:
#    full_name = each + '.sql'
#    if full_name not in file_set:
#        wrong_set.add(full_name)

#for each in sorted(wrong_set):
#    print each

        

        #print name_stripped_extend_name
        #f = open(join(root, each_file), 'r')
        #analyzed_file = analyze_file(f)
        #analyzed_file.demo()
#        print each_file
    
