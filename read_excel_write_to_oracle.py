#!/bin/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function

import cx_Oracle
import xlrd

# Connect as user "hr" with password "welcome" to the "oraclepdb" service running on this computer.
connection = cx_Oracle.connect('yungo_customer','Yungo2016','172.16.1.22:1521/orcl')
# connection = cx_Oracle.connect('yungo_customer/Yungo2016@172.16.1.22:1521/orcl')
# tns = cx_Oracle.makedsn(host='172.19.11.45', port=1526 , service_name='racdb')
# connection = cx_Oracle.connect('yungo_customer', 'Yungo2016', tns)
cursor = connection.cursor()

data = xlrd.open_workbook('test.xlsx', 'r')
sheet0 = data.sheet_by_index(0)
nrows = sheet0.nrows
cacl = 3073
for line in xrange(nrows):
    if line == 0:
        continue
    filter_keyword = sheet0.row_values(line)[0]
    filter_result = sheet0.row_values(line)[1]
    filter_result = filter_keyword if filter_result is None or filter_result == '' else filter_result
    cursor.execute(r'Insert into TD_TPJK_FILTER_WORDS (ID,FILTER_KEYWORD,FILTER_RESULT,ORDER_VAL,FILTER_TYPE,GROUP_CODE) '
                   r'values (:ID,:FILTER_KEYWORD,:FILTER_RESULT,1,1,:GROUP_CODE)',
                   ID=cacl,
                   FILTER_KEYWORD=filter_keyword,
                   FILTER_RESULT=filter_result,
                   GROUP_CODE='carbrand'
                   )
    cacl += 1

connection.commit()
# 关闭cursor
cursor.close()
# 关闭连接
connection.close()
# 查询事例
'''
cursor = connection.cursor()
cursor.execute('select id,email from TD_EMAIL_CONFIG')
for fname, lname in cursor:
    print("Values:", fname, lname)
'''

'''
for line in xrange(nrows):
    if line == 0:
        continue
    print (sheet0.row_values(line)[0] + "," + sheet0.row_values(line)[1])
'''