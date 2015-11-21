#encoding:utf-8
import re
#过滤多行注释，接收多行脚本，返回多行脚本(作为一个整体)
def multipleline_comment_filter(lines):
    cursor_begin = 0
    comment_begin = 0
    comment_end = 0
    out_str = ''
    comment_begin = lines.find('/*', cursor_begin)
    while(comment_begin != -1):
        out_str += lines[cursor_begin:comment_begin]
        comment_end = lines.find('*/',comment_begin + 2)
        cursor_begin = comment_end + 2
        comment_begin = lines.find('/*', cursor_begin)
    out_str += lines[cursor_begin:]
    return out_str

def quotation_filter(lines):
    cursor_begin = 0
    cursor_end = 0
    comment_end = 0
    out_str = []
    comment_begin = lines.find('''\'''')
    while(comment_begin != -1):
        #print comment_begin
        #out_str += lines[cursor_begin:comment_begin]
        #out_str.append(lines[cursor_begin:comment_begin])
        print lines[cursor_begin:comment_begin]
        comment_end = lines.find('''\'''',comment_begin + 1) + 1
        #quotation = lines[comment_begin:comment_end].replace(';', ',')
        #out_str += quotation
        cursor_begin = comment_end
        comment_begin = lines.find('''\'''', cursor_begin)
    #out_str += lines[cursor_begin:]
    out_str.append(lines[cursor_begin:comment_begin])
    return ''.join(out_str)


#过滤单行注释，接收单行脚本，返回单行脚本
def singleline_comment_filter(line):
    if line.find('--') != -1 :
        return line[:line.find('--')]
    else:
        return line


#过滤注释，连续空格，空行，返回以';'为分隔符的list
def comment_filter(lines):
    #print lines
    multi_comment_striped = multipleline_comment_filter(lines)
    multi_comment_striped = quotation_filter(multi_comment_striped)
    discrete_lines = multi_comment_striped.split('\n')
    output_str = ''
    multi_space_pattern = re.compile(r'\s+')
    for line in discrete_lines:
        single_comment_stripped = singleline_comment_filter(line)
        if single_comment_stripped.strip() != '':
            output_str += ' ' + multi_space_pattern.sub(' ',single_comment_stripped.strip('\n'))
    return output_str.split(';')

if __name__ == '__main__':
    #f = open('.\sql\ywc\KHFX_KHPJBQL_KHFHXFBQ_C_012.sql', 'r')
    f = open('test.sql', 'r')
    content = f.read()
    for each in comment_filter(content):
        print each

