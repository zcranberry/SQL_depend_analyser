#encoding:utf-8
import os 
from os.path import join
from sql_parser import analyze_file
from comment import comment_filter
from config_xls_rd import *


data = xlrd.open_workbook('.\input\RDM_AFTER_20151324.xls', encoding_override = 'cp1252')
names = data.sheet_names()

jobs = job_collection()

#读excel的作业配置页
table = data.sheets()[2] #Job Sheet
for i in xrange(1, table.nrows - 1):
    j = job(table.row_values(i))
    jobs.add(j.job_name, j)
###################################################

#读excel的作业依赖配置页
table_job_dependence = data.sheets()[4] #job_dependence sheet
for i in xrange(1, table_job_dependence.nrows - 1):
    line = table_job_dependence.row_values(i)
    target, source = line[0], line[1]
    if target != '13031_LSJS_END_BAK' and source != '13031_LSJS_BGN':
        jobs.job_set[target].add_job_dependence(source)



#读所有的sql脚本
file_dict = dict()
for root, dirs, files in os.walk(".\sql"):
    for each_file in files:
        f = open(join(root, each_file), 'r')
        analyzed_file = analyze_file(f)
        f.close()
        analyzed_file.process_file()
        file_dict[analyzed_file.job_name] = analyzed_file


sorted_keys = sorted(file_dict.keys())
count = 0
for each in sorted_keys:
    depenced_error = False
    if each in jobs.job_set:
        for each_job_dependence in file_dict[each].job_dependence:
            if each_job_dependence not in jobs.job_set[each].job_dependence:
                depenced_error = True
        if depenced_error:
            print 'FAIL'
            count += 1
        else:
            print 'SUCC'

        print each
        file_dict[each].print_result()
        print 'job dependence by ctm'
        print sorted(jobs.job_set[each].job_dependence)
        print ''
    else:
        print 'Job not found:' + each


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
    
#for name, job in jobs.job_set.iteritems():
#    print 'Job_name:' + job.job_name
#    print 'Job_dependence:'
#    print job.job_dependence
#    print ''




#count = 0
#for each_job in jobs.job_set.values():
#    if each_job.consistency_check() != True :
#        print count
#        print each_job
#        print ''
#        count += 1
