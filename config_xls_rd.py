#encoding:utf-8
# 期望功能：深度搜索任务依赖，验证文件依赖，日志路径，作业依赖
import xlrd
import re

class job:
    def __init__(self, line):
        self.jobflow_name, self.job_name, self.cmd_line, self.freq, self.comment, self.log = line[0], line[1], line[3], line[5], line[14], line[15]
        tmpline = re.sub(r'\s+', ' ', self.cmd_line) #去除多余空格
        try: #有不符合xxx_run.sh xxx.sql YYYYMMDD模式的会使sql_name置空 
            self.sql_name = tmpline.split(' ')[1].split('.')[0]
        except:
            self.sql_name = ''
        self.estimate_logfile = r'/rdmetl/log/' + self.jobflow_name.split('_')[1].lower() + r'/%%yyyymmdd./'+self.sql_name + r'.sql.log'

    def __unicode__(self):
        retstr = 'Jobflow_name: ' + self.jobflow_name +  '\nJob_name: ' + self.job_name + '\nCmd_line: ' + self.cmd_line + \
                '\nsql_name: ' + self.sql_name + '\nComment: ' + self.comment + '\nLog:  ' + self.log + '\nLog1: ' + self.estimate_logfile
        return retstr

    def __str__(self):
        return unicode(self).encode('gbk')


    def consistency_check(self):
        if self.jobflow_name + '_' + self.sql_name.upper() != self.job_name:
            return 'JobNameError'
        #if self.estimate_logfile != self.log: #log配错目前较多，暂时不管
        #    return 'LogFileError' 
        return True

class job_collection:
    def __init__(self):
        self.job_set = dict()

    def add(self, name, value):
        self.job_set[name] = value


#class job_visited:
#    def __init__(self, 



if __name__ == '__main__':
    data = xlrd.open_workbook('RDM_AFTER_20151324.xls', encoding_override = 'cp1252')
    names = data.sheet_names()
    table = data.sheets()[2] #Job Sheet
    
    jobs = job_collection()

    #jobs = []

    for i in xrange(1, table.nrows - 1):
        #jobs.append(job(table.row_values(i)))
        j = job(table.row_values(i))
        jobs.add(j.job_name, j)


    count = 0
    for each_job in jobs.job_set.values():
        if each_job.consistency_check() != True :
            print count
            print each_job
            print ''
            count += 1

    
