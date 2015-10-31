#encoding:utf-8
import re
from comment import comment_filter

#需要筛选出来的关键词，以schema名字为特征
keyword_pattern = re.compile(r'\b(lsc|jcc|zbc|ywc|yyc)\.\w+\b', flags=re.IGNORECASE)
#筛选出'from'关键字，以后可能会补充 as 等其他关键字
from_pattern = re.compile(r'from|source_table', flags=re.IGNORECASE)

class analyze_file:
    def __init__(self, input_file):
        self.source = set()
        self.target = set()
        self.input_file = input_file
        self.lines = comment_filter(input_file.read())

    def source_target_finder(self, line):
        keywords = re.finditer(keyword_pattern, line)
        from_word = re.search(from_pattern, line)
        if keywords and from_word:
            for keyword in keywords:
                if  keyword.start() > from_word.start():
                    self.source.add(keyword.group())
                else:
                    self.target.add(keyword.group())

    def process_file(self):
        for line in self.lines:
            self.source_target_finder(line)
        #所有行处理完了之后，去除依赖自身的source,比如dsrzt_khjbxx
        self.source -= self.target

    def print_result(self):
        print 'source:'
        print self.source
        print 'target:'
        print self.target 

    def demo(self):
        print self.input_file
        self.process_file()
        self.print_result()
        print ''

        

if __name__ == '__main__':
    f = open('DSRZT_KHJBXXLSB_L.sql', 'r')
    clean_f = analyze_file(f)
    clean_f.demo()

    

