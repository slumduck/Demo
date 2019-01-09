#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: liangzhang


'''
# pip install xlrd 读excel
'''


from __future__ import print_function
import xlrd
import os
import re


class ParseFile(object):

    # 符合条件的内容
    content = []
    # 读取的文件路径
    file_path = ''
    # 文件类型 -- 文件扩展名
    file_extention = {'txt': ['txt'], 'excel': ['xlsx', 'xls']}

    def __init__(self, file_path):
        # super(ParseFile, self).__init__()
        self.file_path = file_path
    # 逐行读取，返回符合要求的行集合

    def read_line(self, filter_):
        file_type = self._file_type()
        if file_type == 'txt':
            f = TxtOrPureText(self.file_path)
            f.read_line(filter_)
        elif file_type == 'excel':
            f = Excel(self.file_path)
            f.read_line(filter_)
        else:
            print(u'暂不支持的文件格式:%s', file_type)

    # 文件类型
    def _file_type(self):
        for key, value in self.file_extention.items():
            for e in value:
                if self.file_path.endswith(e):
                    return key

    # 提取结果写入文件
    def write(self, target_file):
        if target_file is None:
            target_file = 'password.txt'
        else:
            target_file = target_file + '.txt'
        if os.path.exists(target_file):
            os.remove(target_file)

        try:
            fw = open(target_file, 'a+')
            # fw.writelines(self.content)
            for c in self.content:
                fw.write(c.strip())
                fw.write('\n')
        except Exception as err:
            fw.close()
            print(err)

    # 匹配ip
    def find_ip(self, v_str, row_values_line):
        ip_ = re.match(
            r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))',
            row_values_line)
        if ip_ is not None and ip_.group() == v_str:
            self.content.append(row_values_line)
            return True
        return False


'''
  读取excel
'''


class Excel(ParseFile):

    def read_line(self, filter_):
        data = xlrd.open_workbook(self.file_path, 'r')
        sheet0 = data.sheet_by_index(0)
        nrows = sheet0.nrows
        filter_type = type(filter_)
        for line in xrange(nrows):
            if line == 0:
                continue
            row_values = sheet0.row_values(line, 0)
            row_values_line = '  '.join(row_values)
            #
            if filter_type == list or filter_type == tuple or filter_type == set:
                for f in filter_:
                    if self.find_ip(f, row_values_line):
                        continue
            elif filter_type == str:
                if self.find_ip(filter_, row_values_line):
                    continue
            else:
                print(u'Excel.readLine不支持的参数类型（filter_）：%s', filter_type.__name__)



'''
  读取纯文本
'''


class TxtOrPureText(ParseFile):

    def read_line(self, filter_):
        try:
            f = open(self.file_path, 'r')
            lines = f.readlines()
            if len(lines) == 0:
                f.close()
                print(u'文件%s是空的', self.file_path)
                return
            filter_type = type(filter_)
            for line in lines:
                if line == 0:
                    continue
                #
                if filter_type == list or filter_type == tuple or filter_type == set:
                    for f in filter_:
                        if self.find_ip(f, line):
                            continue
                elif filter_type == str:
                    if self.find_ip(filter_, line):
                        continue
                else:
                    print(u'Excel.readLine不支持的参数类型（filter_）：%s', filter_type.__name__)
        except Exception as err:
            f.close()
            print(err)


if __name__ == '__main__':
    # 目标文件
    excel = u'E:\python\Demo\password.xlsx'
    txt = u'新密码_20181206.txt'
    p = ParseFile(txt)
    p.read_line([
        '172.19.12.64', # 太平
        '172.19.12.66', # 德邦
        '172.19.12.70', # 德邦
        '172.19.12.71', # 圆通
        '172.19.12.77', # push
        '172.19.12.78', # 德邦
        '172.19.11.31', # brain push
        '172.19.11.32', # brain push Nginx
        '172.19.11.65', # brain push
        '172.19.11.66'  # 太平
        ])
    # 要提取的ip
    # for x in p.content:
    #    print(x)
    p.write('zhangliang')
    '''
    ip = re.match(
        r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))',
        '172.19.11.2 root zpmu7Bj_VQSnxWqsmI')
    if ip:
        print(ip)
    else:
        print('no')
    '''
