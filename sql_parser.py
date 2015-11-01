#encoding:utf-8
import re
from comment import comment_filter

#需要筛选出来的关键词，以schema名字为特征
keyword_pattern = re.compile(r'\b(lsc|jcc|zbc|ywc|yyc)\.\w+\b', flags=re.IGNORECASE)
#筛选出'from'关键字，以后可能会补充 as 等其他关键字
from_pattern = re.compile(r'from|job_dependence_table', flags=re.IGNORECASE)

class analyze_file:
    def __init__(self, input_file):
        self.job_dependence = set()
        self.target = set()
        self.input_file = input_file
        self.lines = comment_filter(input_file.read())
        #以下信息都可以从文件名及路径中推测出来
        self.whole_name = input_file.name                   #whole_name like 'e:\dir\jcc\DSRZT_KHJBXX.sql'
        self.name = self.whole_name.split('\\')[-1]         #DSRZT_KHJBXX.sql
        self.schema = self.whole_name.split('\\')[-2]       #jcc
        self.table_name = self.name.split('.')[0]           #DSRZT_KHJBXX
        self.subname = self.table_name.split('_')[0]        #DSRZT
        self.jobflow_name = str.upper('13031' + '_' + self.schema + '_' + self.subname) #13031_JCC_DSRZT
        self.file_dependcy = ''
        self.job_name = str.upper(self.jobflow_name + '_' + self.table_name)  #13031_JCC_DSRZT_DSRZT_KHJBXX
        

    def job_dependence_finder(self, line):
        keywords = re.finditer(keyword_pattern, line)
        from_word = re.search(from_pattern, line)
        if keywords and from_word:
            for keyword in keywords:
                if  keyword.start() > from_word.start():
                    self.job_dependence.add(keyword.group())
                else:
                    self.target.add(keyword.group())

    #load层大部分没有sql脚本，无法通过sql文件来判断，只能通过ctm配置中的表名来找
    def file_dependence_finder(self):
        pass

    def filename_target_check(self):
        pass

    def jobname_estimate(self):
        self.job_name = '13031' + '_' + schema +  '_'+ self.subname


    def process_file(self):
        for line in self.lines:
            self.job_dependence_finder(line)
        #所有行处理完了之后，去除依赖自身的job_dependence,比如dsrzt_khjbxx
        #self.job_dependence -= self.target

    def print_result(self):
        print 'job_dependence:'
        print self.job_dependence
        print 'target:'
        print self.target 

    def demo(self):
        print 'schema:', self.schema, 'table:', self.table_name, 'jobflow_name:', self.jobflow_name, 'job_name:', self.job_name
        self.process_file()
        self.print_result()
        print ''

        

if __name__ == '__main__':
    f = open('DSRZT_KHJBXXLSB_L.sql', 'r')
    clean_f = analyze_file(f)
    clean_f.demo()

    

