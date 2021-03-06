#encoding:utf-8
# 期望功能：深度搜索任务依赖，验证文件依赖，日志路径，作业依赖
import xlrd
import re

class Job:
    def __init__(self, line):
        self.jobflow_name, self.job_name, self.cmd_line, self.freq, self.comment, self.log = line[0], line[1], line[3], line[5], line[14], line[15]
        self.file_dependence = None
        self.job_dependence = set()
        tmpline = re.sub(r'\s+', ' ', self.cmd_line) #去除多余空格
        try: #有不符合xxx_run.sh xxx.sql YYYYMMDD模式的会使sql_name置空 
            if tmpline.find('py.sh') != -1: #py.sh DD XXXX.sql YYYYMMDD
                useful_parts = tmpline.split(' ')[2:] #跳掉py.sh DD
                tmpline = ' '.join(useful_parts)
            self.sql_name = tmpline.split(' ')[1].split('.')[0]
        except:
            #print self.job_name
            self.sql_name = ''
        self.estimate_logfile = r'/rdmetl/log/' + self.jobflow_name.split('_')[1].lower() + r'/%%yyyymmdd./'+self.sql_name + r'.sql.log'


    def add_job_dependence(self, src):
        self.job_dependence.add(src)


    def consistency_check(self):
        if self.jobflow_name + '_' + self.sql_name.upper() != self.job_name:
            return 'JobNameError'
        #if self.estimate_logfile != self.log: #log配错目前较多，暂时不管
        #    return 'LogFileError' 
        return True

    def __unicode__(self):
        retstr = 'Jobflow_name: ' + self.jobflow_name +  '\nJob_name: ' + self.job_name + '\nCmd_line: ' + self.cmd_line + \
                '\nsql_name: ' + self.sql_name + '\nComment: ' + self.comment + '\nLog:  ' + self.log + '\nLog1: ' + self.estimate_logfile
        return retstr

    def __str__(self):
        return unicode(self).encode('gbk')

class JobCollection:
    def __init__(self):
        self.job_set = dict()

    def add(self, name, value):
        self.job_set[name] = value



#class job_visited:
#    def __init__(self, 

#####################################################################################################################################

#class job_dependence_edge:#一条边
#    def __init__(self, line):
#        self.edge_start, self.edge_end = line
#        if self.edge_start != '13031_LSJS_END_BAK' and self.edge_end != '13031_LSJS_BGN': #纯技术作业，过滤掉
#            pass
#
#
#
#class node:#一个节点
#    def __init__(self, name):
#        self.name = name
#        self.src = set()
#        self.target = set()
#    
#    def add_src(self, src):
#        self.src.add(src)
#
#    def add_target(self, target):
#        self.target.add(target)
#
#    def demo(self):
#        print 'Name: ' + self.name
#        print 'Src: '
#        for each in self.src:
#            print each
#        print 'target:'
#        for each in self.target:
#            print each
#        print ''

#class node_collections:
#    def __init__(self):
#        self.nodes= dict()
#    #def add_node(self, node):
#    #    self.nodes[node] = node()


#class job_dependece_graph:
#    def __init__(self):
#        self.graph_edges = set()
#        self.graph_nodes = node_collections()
#
#    def add_edge(self, edge):
#        #self.graph_edges.add(edge)
#        target, src = edge[0], edge[1]
#        if target not in self.graph_nodes.nodes:
#            self.graph_nodes.nodes[target] = node(target)
#
#        if src not in self.graph_nodes.nodes:
#            self.graph_nodes.nodes[src] = node(src)
#
#        self.graph_nodes.nodes[src].add_target(target) # 用节点还是名字待定
#        self.graph_nodes.nodes[target].add_src(src)





if __name__ == '__main__':
    data = xlrd.open_workbook('.\input\RDM_AFTER_20151324.xls', encoding_override = 'cp1252')
    names = data.sheet_names()
    table = data.sheets()[2] #Job Sheet
    
    jobs = JobCollection()


    for i in xrange(1, table.nrows - 1):
        #jobs.append(job(table.row_values(i)))
        j = Job(table.row_values(i))
        jobs.add(j.job_name, j)


    count = 0
    for each_job in jobs.job_set.values():
        if each_job.consistency_check() != True :
            print count
            print each_job
            print ''
            count += 1
################################################## 
    #table = data.sheets()[4]
    #graph = job_dependece_graph()

    #for i in xrange(1, table.nrows - 1):
    #    graph.add_edge(table.row_values(i))

    #for each in graph.graph_nodes.nodes:
    #    graph.graph_nodes.nodes[each].demo()

    
