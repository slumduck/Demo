#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from kafka import KafkaProducer


def producer(servers, topic, messge):
    producer = KafkaProducer(bootstrap_servers=servers)
    msg = json.dumps(messge)
    for i in range(1000):
        producer.send(topic, msg, partition=0)
    producer.close()


if __name__ == '__main__':

    msg_dict = r'''{
      "task_name": "转人工测试",
      "cluster": "yeta",
      "taskdataid": "35044434454384640",
      "role": "ccc",
      "session_proto_specific_hangup_cause": "sip:200",
      "line": "sofia/external/18715153022@172.16.1.69:5060",
      "session_sip_to_host": "172.16.1.69",
      "session_billsec": "33",
      "FROM": "fs-inbound@172.16.1.36:8021",
      "session_sip_hangup_disposition": "recv_bye",
      "session_duration": "49",
      "session_other_type": "originator",
      "session_sip_call_id": "4f6062fb-787e-1237-3eaf-20474793b45c",
      "host": "kxjl-test1",
      "id": "30b457f1-dcda-43f5-89df-a8ed2234de33",
      "dnis": "18715153022",
      "event": "call_end",
      "calluuid": "7801f0f4-fddb-11e8-b313-059e34ad4c93",
      "ani": "69102939",
      "taskid": "547569287366720",
      "timestamp": "1544598017881",
      "direction": "in",
      "session_bridge_uepoch": "1544597973629262",
      "business_name": "10525企业",
      "process": "ccc",
      "session_answersec": "16",
      "call_direction": "out",
      "businessid": "10525",
      "datacenter": "hefei",
      "session_end_uepoch": "1544598017849279",
      "session_answer_uepoch": "1544597984569245",
      "service": "call",
      "speechskill_name": "转人工计费",
      "TO": "ccc@172.16.1.36:8021",
      "subevent": "CHANNEL_DESTROY",
      "session_sip_from_host": "172.16.1.36",
      "session_other_calluuid": "9d8f3f36-f19d-4153-9add-c8ff08986438",
      "speechskillid": "6181",
      "session_start_uepoch": "1544597968769260"
    }'''
    #producer(['172.16.1.30:9092', '172.16.1.30:9093', '172.16.1.30:9094'], 'fee-transfer-people', msg_dict)
    print(msg_dict)
