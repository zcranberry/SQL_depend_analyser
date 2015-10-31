#encoding:utf-8
import re
def multipleline_comment_filter(lines):
    cursor_begin = 0
    comment_begin = 0
    comment_end = 0
    out_str = ''
    comment_begin = lines.find('/*', cursor_begin)
    while(comment_begin != -1):
        out_str += lines[cursor_begin:comment_begin]
        comment_end = lines.find('*/',comment_begin) + 2
        cursor_begin = comment_end
        comment_begin = lines.find('/*', cursor_begin)
    out_str += lines[cursor_begin:]
    return out_str


def singleline_comment_filter(line):
    if line.find('--') != -1 :
        return line[:line.find('--')]
    else:
        return line

if __name__ == '__main__':
    f = open('KHFX_KHPJBQL_KHCYCPBQ_D.sql', 'r')
    content = f.read()
    multi_comment_striped = multipleline_comment_filter(content)
    lines = multi_comment_striped.split('\n')
    output_str = ''
    multi_space_pattern = re.compile(r'\s+')
    for line in lines:
        single_comment_stripped = singleline_comment_filter(line)
        if single_comment_stripped.strip() != '':
            output_str += multi_space_pattern.sub(' ',single_comment_stripped.strip('\n'))
    output_list = output_str.split(';')
    #for segment in output_list:
    #    print segment + ';'


    source = set()
    target = set()
    white_list_pattern = re.compile(r'(\b(lsc|jcc|zbc|ywc|yyc)\.\w+\b)', flags=re.IGNORECASE)
    from_pattern = re.compile(r'from', flags=re.IGNORECASE)
    #print from_pattern
    for segment in output_list:
        m = re.findall(white_list_pattern, segment)
        from_m = re.search(from_pattern, segment)
        #print type(from_m)
        #print from_m
        #print re.findall(white_list_pattern, segment)
        #print m
        if m != [] and from_m:
            for each in m:
            #    print segment.find(each[0])
                if segment.find(each[0]) > segment.find(from_m.group()[0]):
                    source.add(each[0])
                else:
                    target.add(each[0])

    
    for target_element in target:
        source.remove(target_element)
    print 'source:'
    print source
    print 'target:'
    print target



