#!/bin/bin/python2
# -*- coding: UTF-8 -*-

from __future__ import print_function

import urllib2
import json
import chardet
import time
import xlrd


def change_utf8(data):
    code = chardet.detect(data)['encoding']
    data = data.decode(code).encode('UTF-8')
    return data


headers = {
 'Accept': 'application/json',
 'Content-Type': 'application/json',
 'Connection': 'keep-alive'
}


def read_xsl():
    data = xlrd.open_workbook('taiping1114-1115.xlsx', 'r')
    sheet0 = data.sheet_by_index(0)
    nrows = sheet0.nrows
    for line in xrange(nrows):
        if line == 0:
            continue
        calluuid = sheet0.row_values(line)[0]
        try:
            # 从大数据平台获取录音
            voice = get_voice(calluuid)
            # 推送录音给客户
            push_vocie(voice)
        except Exception, e:
            print(e.message)
            print('推送录音异常，calluuid：%s'%(calluuid))


def get_voice(calluuid):

    t_url = 'http://172.19.11.118:8992/taichi-data-api/api/v1/session/167/querySession'
    t_data = {
            "query": "calluuid:" + calluuid,
            "index": 0,
            "size": 1,
            "includes": ["ant_mediapath", "brain_calluuid", "session_thirduuid", "ant_begintime", "brain_callee", "brain_userdata"]
        }
    req = urllib2.Request(t_url, json.dumps(t_data, encoding='utf-8'), headers=headers)
    response = urllib2.urlopen(req)
    str_response = response.read()
    # print(str_response)
    dict_response = json.loads(change_utf8(str_response))
    code = dict_response['code']
    if code != 0:
        print('从大数据平台，获取录音失败,calluuid : %s'%(calluuid))
        return None
    result = dict_response.get('result')
    if result is not None:
        rows = result.get('rows')
        if len(rows) > 0:
            call_uuid = rows[0].get('brain_calluuid')
            ant_mediapath = rows[0].get('ant_mediapath')
            if call_uuid is None or ant_mediapath is None:
                print('无录音,calluuid : %s'%(calluuid))
                return None
            sessionid = rows[0].get('session_thirduuid')
            brain_userdata = rows[0].get('brain_userdata')
            if sessionid is None and brain_userdata is None:
                print('无sessionid或brain_userdata,calluuid : %s'%(calluuid))
                return None
            if sessionid is None:
                rows[0]['session_thirduuid'] = brain_userdata
            brain_callee = rows[0].get('brain_callee')
            if brain_callee is None:
                print('无brain_callee,calluuid : %s'%(calluuid))
                return None
            return rows[0]
        else:
            print('无录音,calluuid : %s'%(calluuid))
            return None
    else:
        print('从大数据平台，获取录音失败,calluuid : %s'%(calluuid))
        return None


def push_vocie(body):
    if body is None:
        print('推送数据失败，无body。。。。')
        return None
    t_url = 'http://172.19.11.32:8106/kxjl-push-api/api/v1/push/' \
            + body.get('brain_callee') \
            + '/VOICE_PUSH/recordDataPush'
    t_data = {
            "dateTime": longtime_strtime(body['ant_begintime']),
            "voicePath": body['ant_mediapath'],
            "sessionId": body['session_thirduuid'].replace('|', ''),
            "callUUID": body['brain_calluuid']
        }
    req = urllib2.Request(t_url, json.dumps(t_data, encoding='utf-8'), headers=headers)
    response = urllib2.urlopen(req)
    str_response = response.read()
    dict_response = json.loads(change_utf8(str_response))
    code = dict_response['code']
    if code != 0:
        print('推送录音失败,calluuid : %s'%(body.get('brain_calluuid')))
        return None
'''
13位毫秒
'''


def longtime_strtime(longtime):
    # 获得当前时间时间戳
    #timeStamp = int(time.time())
    timeStamp = float(float(longtime) / 1000)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
    return strTime


if __name__ == '__main__':
    #read_xsl()
    # 从大数据平台获取录音
    #voice = get_voice('01PK3KHLJ8DSV2DH345H7B5AES065KO5')
    # 推送录音给客户
    #push_vocie(voice)
    #longtime_strtime(1542198258000)

    no_sessionid = ['01PK3KHLJ8DSV2DH345H7B5AES06469I',
                    '01PK3KHLJ8DSV2DH345H7B5AES06469I',
                    '01PK3KHLJ8DSV2DH345H7B5AES06469I',
                    '01PK3KHLJ8DSV2DH345H7B5AES06469I',
                    '01PK3KHLJ8DSV2DH345H7B5AES063T9O',
                    '01PK3KHLJ8DSV2DH345H7B5AES0650G6',
                    '01PK3KHLJ8DSV2DH345H7B5AES066MN8',
                    '01PK3KHLJ8DSV2DH345H7B5AES066FC4',
                    '01PK3KHLJ8DSV2DH345H7B5AES066EN6',
                    '01PK3KHLJ8DSV2DH345H7B5AES066DL1',
                    '01PK3KHLJ8DSV2DH345H7B5AES066A13',
                    '01PK3KHLJ8DSV2DH345H7B5AES0666S8',
                    '01PK3KHLJ8DSV2DH345H7B5AES066228',
                    '01PK3KHLJ8DSV2DH345H7B5AES067E86',
                    '01PK3KHLJ8DSV2DH345H7B5AES0675HQ',
                    '01PK3KHLJ8DSV2DH345H7B5AES06751B',
                    '01PK3KHLJ8DSV2DH345H7B5AES0674RM',
                    '01PK3KHLJ8DSV2DH345H7B5AES066PRK']
    for id in no_sessionid:
        try:
            print('推送开始。。。。')
            print('calluuid：%s'%(id))
            voice = get_voice(id)
            push_vocie(voice)
            print('推送结束。。。。')
        except Exception, e:
            print(e.message)
            print('推送录音异常，calluuid：%s'%(id))