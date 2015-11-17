#encoding:utf-8
import re
from comment import comment_filter

#需要筛选出来的关键词，以schema名字为特征
keyword_pattern = re.compile(r'\b(LSC|JCC|ZBC|YWC|YYC)\.\w+\b', flags = re.IGNORECASE)
#筛选出'from'关键字，以后可能会补充 as 等其他关键字
from_pattern = re.compile(r'FROM|SOURCE_TABLE', flags = re.IGNORECASE)
#筛选出视图（主要是指标层的资产负债）
view_pattern = re.compile(r'VIEW_KHHZ_\w+(Y|N)RJ_(D|M|C)', flags = re.IGNORECASE)

black_list = set()
black_list.add('13031_JCC_GGZT_GGZT_BZDMB')
black_list.add('13031_JCC_GGZT_GGZT_BZDMYSB')

class analyze_file:
    def __init__(self, input_file):
        self.table_dependence = set()
        self.job_dependence = set()
        self.target = set()
        self.input_file = input_file
        self.lines = comment_filter(input_file.read())
        #以下信息都可以从文件名及路径中推测出来
        self.whole_name = str.upper(input_file.name)        #whole_name like 'e:\dir\jcc\DSRZT_KHJBXX.sql'
        self.name = self.whole_name.split('\\')[-1]         #DSRZT_KHJBXX.sql
        self.schema = self.whole_name.split('\\')[-2]       #jcc
        self.table_name = self.name.split('.')[0]           #DSRZT_KHJBXX
        self.subname = self.table_name.split('_')[0]        #DSRZT
        if self.schema in ('UNLOAD', 'YYC') and self.subname not in ('ACRM', 'OCRM', 'EDIP', 'FPAA', 'LSBB', 'WYSJYH', 'TYBB'):
            self.subname = 'OTHER'
        if self.schema == 'ZBC':
            self.subname = self.table_name.split('_')[1]    #指标层的命名不对，不过错误的模式是固定的。
        self.jobflow_name = str.upper('13031' + '_' + self.schema + '_' + self.subname) #13031_JCC_DSRZT
        self.file_dependcy = ''
        self.job_name = str.upper(self.jobflow_name + '_' + self.table_name)  #13031_JCC_DSRZT_DSRZT_KHJBXX
        self.process_file()
        

    def table_dependence_finder(self, line):
        keywords = re.finditer(keyword_pattern, line)
        from_word = re.search(from_pattern, line)
        if keywords and from_word:
            for keyword in keywords:
                keyword_literal = keyword.group().upper() # JCC.DSRZT_KHJBXX
                schema_literal ,table_without_schema_literal = keyword_literal.split('.') # JCC,  DSRZT_KHJBXX

                view_word = re.search(view_pattern, table_without_schema_literal)
                if view_word:  #视图需转换成相应的表
                    table_without_schema_literal = table_without_schema_literal.replace('VIEW', 'HZZBC').replace('RJ_','JS_')

                sub_schema_literal = table_without_schema_literal.split('_')[0]  #DSRZT
                if schema_literal == 'LSC': #临时层有特殊的命名技巧
                    schema_literal = 'LOAD'
                    if sub_schema_literal not in ('EDW', 'OCRM', 'ACRM' ,'GAFEYWK', 'RPHM', 'MA', 'SMS'):
                        sub_schema_literal = 'OTHER'
                elif schema_literal == 'ZBC':
                    sub_schema_literal = table_without_schema_literal.split('_')[1]

                alist = ['13031', schema_literal, sub_schema_literal, table_without_schema_literal]
                estimated_jobname = '_'.join(alist)   #13031_JCC_DSRZT_DSRZT_KHJBXX
                if  keyword.start() > from_word.start():
                    self.table_dependence.add(keyword_literal)
                    self.job_dependence.add(unicode(estimated_jobname))
                else:
                    self.target.add(estimated_jobname)

        
    def sqlname_target_check(self):
        pass
    #load层大部分没有sql脚本，无法通过sql文件来判断，只能通过ctm配置中的表名来找
    def file_dependence_finder(self):
        pass

    def filename_target_check(self):
        pass

    def process_file(self):
        for line in self.lines:
            self.table_dependence_finder(line)
        #所有行处理完了之后，去除依赖自身的table_dependence,比如dsrzt_khjbxx
        self.job_dependence -= self.target
        self.job_dependence -= black_list 

    def print_result(self):
        print 'job dependence by sql:'
        #print self.table_dependence
        print sorted(self.job_dependence)
        #print 'target:'
        #print self.target 

    def demo(self):
        print 'schema:', self.schema, 'table:', self.table_name, 'jobflow_name:', self.jobflow_name, 'job_name:', self.job_name
        #self.process_file()
        self.print_result()
        print ''

        

if __name__ == '__main__':
    f = open('.\sql\zbc\HZZBC_KHHZ_KHKNZCFZNJS_C.sql', 'r')
    clean_f = analyze_file(f)
    clean_f.demo()

    

