#encoding:utf-8
import re
MAX_INT = 2 ** 32
multi_space_pattern = re.compile(r'\s+')

def negative_trans(num):
    if num == -1:
        return MAX_INT
    else:
        return num

def strip_sql_comment(byte_stream):
    cursor_begin = 0
    multi_comment_begin = byte_stream.find('/*', cursor_begin)
    quotation_begin = byte_stream.find('''\'''', cursor_begin)
    single_comment_begin = byte_stream.find('--', cursor_begin)
    out_str = []
    while(multi_comment_begin + quotation_begin + single_comment_begin != -3):     #三种符号均找不到
        #至少找到一个
        #print ' Multi:' + str(multi_comment_begin) + ' Quote:' + str(quotation_begin) + ' Single:' + str(single_comment_begin)
        multi_comment_begin, single_comment_begin, quotation_begin = map(negative_trans, [multi_comment_begin, single_comment_begin, quotation_begin])
        min_pos = min(multi_comment_begin, single_comment_begin, quotation_begin)
        out_str.append(byte_stream[cursor_begin:min_pos])
        if min_pos == multi_comment_begin:          #mode = 'MULTI'
            multi_comment_end = byte_stream.find('*/', min_pos + 2)
            cursor_begin = multi_comment_end + 2
        elif min_pos == quotation_begin:            #mode = 'QUOTE'
            quotation_end  = byte_stream.find('''\'''', min_pos + 1)
            cursor_begin = quotation_end + 1
            out_str.append(byte_stream[quotation_begin:cursor_begin].replace(';', ','))
        elif min_pos == single_comment_begin:       #mode = 'SINGLE'
            single_comment_end = byte_stream.find('\n', min_pos + 2)
            cursor_begin = single_comment_end + 1
        multi_comment_begin = byte_stream.find('/*', cursor_begin)
        quotation_begin = byte_stream.find('''\'''', cursor_begin)
        single_comment_begin = byte_stream.find('--', cursor_begin)
    out_str.append(byte_stream[cursor_begin:])
    final_str = ''.join(out_str)
    return multi_space_pattern.sub(' ', final_str).split(';')

if __name__ == '__main__':
    f = open('.\sql\ywc\KHFX_KHPJBQL_KHFHXFBQ_C_012.sql', 'r')
    content = strip_sql_comment(f.read())
    for each in content.split(';'):
        print each
