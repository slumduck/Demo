#!/usr/bin/env python
# -*- coding:utf-8 -*-

# pip install chardet 安装chardet包

import chardet
import sys

'''
获取字符串的编码类型
对于文件获取一次就可以了
'''


def getcode(str):
    code = chardet.detect(str)['encoding']
    return code


def change_to_utf8(file):
    # C:\Users\Administrator\Desktop\test\tts_list -1.txt
    try:
        f = open(file, 'r')
        text = f.read()
        if len(text) == 0:
            f.close()
            return
        else:
            code = getcode(text)
            codelist = ['utf8', 'utf-8']
            for c in codelist:
               if c == code.lower():
                   print ('已是utf8，无需更改')
                   return
            chinesecode = ['gb2312', 'gb18032', 'gb18030', 'gbk']
            for a in chinesecode:
                if a == code.lower():
                    code = 'GBK'
            text = text.decode(code).encode('UTF-8')
        f.close()
        try:
            fw = open(file, 'w')
            fw.write(text)
        except Exception,e:
            fw.close()
        print ('更改文件编码成功')
    except Exception, e:
        print('更改文件编码异常')
        print e
    finally:
        f.close()


if __name__ == '__main__':
    # change_to_utf8('C:\\Users\\Administrator\\Desktop\\tts_list.txt')
    print sys.getdefaultencoding()
    print sys.getfilesystemencoding()
    print sys.getcheckinterval()