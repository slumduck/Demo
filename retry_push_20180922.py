#!/bin/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function

import cx_Oracle
import urllib2
import json
import chardet

def changeToUTF8(data):

    code = chardet.detect(data)['encoding']
    data = data.decode(code).encode('UTF-8')
    return data

tns = cx_Oracle.makedsn(host='172.19.11.45', port=1526 , service_name='racdb')
connection = cx_Oracle.connect('yungo_customer', 'Yungo2016', tns)
fail = connection.cursor()
failCount = connection.cursor()
update = connection.cursor
# 获取20180922未推送成功的数据
# t.callUUID in ('01L0VT5F34DKT7O7345H7B5AES0A9QHV','01L0VT5F34DKT7O7345H7B5AES0A9PV6','01L0VT5F34DKT7O7345H7B5AES0A9Q3L') and
fail.execute(r'''select t.id,t.calluuid,t.bossapi_url,t.bossapi_callinfo from TD_YYFF_OPERLOG t
                       where t.module = '3446PUSH' and
                       t.create_time < 1537632000000 and 
                       t.create_time >= 1537545600000 and 
                       t.call_success = 0'''
                   )
# 获取未推送成功的条数:
# 01L0VT5F34DKT7O7345H7B5AES0A9EQI(1537578044-536703|80145475)、
# 01L0VT5F34DKT7O7345H7B5AES0A9QHV(1537580375-540472|80144920)、
# 01L0VT5F34DKT7O7345H7B5AES0A9PV6(1537580311-18216|80145196)
# 01L0VT5F34DKT7O7345H7B5AES0A9Q3L(1537580335-18257|80144950)
# t.create_time <= 1537718399000 and
failCount.execute(r'''select count(1) from TD_YYFF_OPERLOG t
                               where t.module = '3446PUSH' and
                               
                               t.create_time >= 1537718400000 and 
                               t.call_success = 0 order by t.create_time asc '''
                   )
# c/blob字段无法通过fetchall/fetchmany获取,一种解决方案是将clob/blob转为字符串，另一种是使用fetchone
# result = cursor.fetchall()
updateSql = r'''
                update TD_YYFF_OPERLOG t set 
                   t.bossapi_returncode = :returncode and 
                   t.bossapi_returninfo = :returninfo and
                   t.call_success = :success
                where t.id = :id'''
# update.prepare(updateSql)
headers = {
 'Accept': 'application/json',
 'Content-Type': 'application/json',
 'Connection': 'keep-alive'
}
''''''
i = 0
count = failCount.fetchone()
totalCount = count[0]
while True:
    if i > 50:
        break
    rr = fail.fetchone()
    print(rr)
    id = rr[0]
    callUUID = rr[1]
    url = rr[2]
    # print(url.strip())
    data = rr[3].read()
    dict_data = json.loads(changeToUTF8(data))
    dict_data.pop('callUUID')
    # ensure_ascii=False 不设置json.dumps()输出的中文输出为Unicode码
    str = json.dumps(dict_data, encoding='utf-8')
    req = urllib2.Request(url, str, headers=headers)
    response = urllib2.urlopen(req)
    str_response = response.read()
    print(str_response)
    '''
    dict_response = json.loads(changeToUTF8(str_response))
    code = dict_response['code']
    if code != 0 and code != -1:
        code = -1
    # 推送成功表
    update.execute(updateSql, {'returncode': code, 'returninfo': str_response, 'success': code})
    connection.commit()
    '''
    i += 1

'''
t_url = 'http://172.19.11.32:8071/platform/prodService/recieve/trace'
t_data = '{}'
req = urllib2.Request(t_url, t_data.strip())
response = urllib2.urlopen(req)
str_response = response.read()
print(str_response)
dict_response = json.loads(changeToUTF8(str_response))
code = dict_response['code']
'''
# 关闭cursor
update.close()
failCount.close()
fail.close()
# 关闭连接
connection.close()

