#encoding:utf-8
import xlrd

class job:
    def __init__(self, line):
        self.jobflow_name, self.job_name, self.cmd_line, self.freq, self.comment, self.log = line[0], line[1], line[3], line[5], line[14], line[15]
        try:
            self.sql_name = self.cmd_line.split(' ')[1].split('.')[0]
        except:
            self.sql_name = ''

    def __unicode__(self):
        retstr = 'Jobflow_name: ' + self.jobflow_name +  '\nJob_name: ' + self.job_name + '\nCmd_line: ' + self.cmd_line + '\nsql_name: ' + self.sql_name + '\nComment: ' + self.comment + '\nLog: ' + self.log
        return retstr

    def __str__(self):
        return unicode(self).encode('gbk')

if __name__ == '__main__':
    data = xlrd.open_workbook('ctm_config.xls', encoding_override = 'cp1252')
    names = data.sheet_names()
    table = data.sheets()[2] #Job Sheet
    
    jobs = []
    for i in xrange(1, 955):
        jobs.append(job(table.row_values(i)))
    

    count = 0
    for each_job in jobs:
        if each_job.jobflow_name + '_' + each_job.sql_name != each_job.job_name:
            print count
            print each_job
            print ''
            count += 1

    
