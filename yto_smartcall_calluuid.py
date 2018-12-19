#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import urllib2
import json
import chardet
import time
import os
import xlwt

headers_json = {
 'Accept': 'application/json',
 'Content-Type': 'application/json',
 'Connection': 'keep-alive'
}


def change_utf8(data):
    code = chardet.detect(data)['encoding']
    data = data.decode(code).encode('UTF-8')
    return data



'''
通过时间获取该通电话的详细信息
'''


def get_call_infomation_by_time(qeury_data):
    url = 'http://172.19.11.92/taiji-data/search'
    req = urllib2.Request(url, json.dumps(qeury_data, encoding='utf-8'), headers=headers_json)
    response = urllib2.urlopen(req)
    str_response = response.read()
    # print(str_response)
    dict_response = json.loads(change_utf8(str_response))
    code = dict_response['totalCount']
    if code <= 0:
        print ('暂无录音。。。。。。。')
        return None
    result = dict_response.get('data')
    if isinstance(result, list):
        return result


'''
提取结果
'''


def deal_result_yto_smartcall(data):
    for x in data:
        session_calluuid = x.get('session_calluuid')
        if session_calluuid is None:
            print(u'该通电话无calluuid。。。')
        brain_extention = json.loads(x.get('brain_extention'))
        call_id = brain_extention.get('call_id')
        callee = brain_extention.get('callee')


class ExcelUtil(object):
    def __init__(self):
        # 创建workbook和sheet对象
        self.workbook = xlwt.Workbook(encoding='UTF-8')

    # 将数据写入Excel
    def write_to_file(self, dir_, data):
        if len(data) == 0:
            return
        # 注意Workbook的开头W要大写
        sheet1 = self.workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        for x, row in enumerate(data):
            session_calluuid = row.get('session_calluuid')
            if session_calluuid is None:
                print(u'该通电话无calluuid。。。')
            brain_extention = json.loads(row.get('brain_extention'))
            call_id = brain_extention.get('call_id')
            for y in [0, 1]:
                sheet1.col(y).width = 256 * 40
                if y == 0:
                    sheet1.write(x, y, session_calluuid)
                if y == 1:
                    sheet1.write(x, y, call_id)
        excel_path = dir_ + os.path.sep + "00103.xls"
        self.workbook.save(excel_path)


if __name__ == '__main__':
    query_val = {
        "begintime": 1543680000000,
        "endtime": 1543766399000,
        "index": 0,
        "order": "_score desc,begintime desc",
        # lucene查询参数，录音时长大于45秒的
        "query": "00103",
        "size": 2000
    }
    data = get_call_infomation_by_time(query_val)
    excel = ExcelUtil()
    excel.write_to_file("E:/", data)

