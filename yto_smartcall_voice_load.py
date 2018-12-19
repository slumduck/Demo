#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import urllib2
import json
import chardet
import time
import os

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
        ant_mediapath = x.get('ant_mediapath')
        if ant_mediapath is None:
            print(u'session_calluuid为%s,无录音。。。' %(session_calluuid))
        brain_extention = json.loads(x.get('brain_extention'))
        waybill_No = brain_extention.get('Waybill_No')
        callee = brain_extention.get('callee')
        caller = brain_extention.get('caller')
        session_begintime = x.get('session_begintime')
        print(u'呼入时间：%s，单号：%s，主叫号：%s，录音路径：%s' % (session_begintime, waybill_No, caller, ant_mediapath))
        # 下载录音，并保存。
        # 文件名：呼入时间+单号+手机号
        if not os.path.exists(callee):
            os.mkdir(callee)
        absolute_path = callee + '/' + longtime_strtime(session_begintime, '%Y-%m-%dT%H-%M-%S') + ',billno ' + waybill_No + ',phone ' + caller + '.wav'
        load_voice(ant_mediapath, absolute_path)
'''
录音下载
'''


def load_voice(voice_path, path):
    url = 'http://172.19.11.100:8080/' + voice_path
    try:
        if os.path.exists(path):
            print(u'当前文件已存在：%s,跳过。。。。。。。'%(path))
            return
        res = urllib2.urlopen(url)
        data = res.read()
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        print(u'录音：%s' %(voice_path))
        print(e)


def longtime_strtime(longtime, date_format_str):
    # 获得当前时间时间戳
    #timeStamp = int(time.time())
    timeStamp = float(float(longtime) / 1000)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(timeStamp)
    strTime = time.strftime(date_format_str, timeStruct)
    return strTime


if __name__ == '__main__':
    query_val = {
        "begintime": 1543248000000,
        "endtime": 1543388399999,
        "index": 0,
        "order": "_score desc,begintime desc",
        # lucene查询参数，录音时长大于45秒的
        "query": "00103 AND playapplicationduration:[45 TO *]",
        "size": 100
    }
    deal_result_yto_smartcall(get_call_infomation_by_time(query_val))
    # get_call_infomation_by_time(query_val)
    #load_voice('ant/2/ivr/0/2018/11/28/0/47262789-EE560C994E347BF7C0063D0892ED4FFC.wav', '0101/test.wav')

