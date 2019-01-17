#!/usr/bin/env python2
# -*- coding:utf-8 -*-


import time
import os
import json
import urllib
import urllib2

import logging
logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

_ipfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"ip.txt")

# 详见 : https://support.dnspod.cn/Kb/showarticle/tsid/227/
login_token = "your_token"
# 详见 : https://www.dnspod.cn/docs/records.html#record-modify
domains = [
    {"login_token": login_token, "sub_domain": "sub1", "domain_id": 100, "record_id": 101,
        "record_type": "AAAA", "value": "", "format": "json", "record_line": "默认"},
    {"login_token": login_token, "sub_domain": "sub2", "domain_id": 102, "record_id": 103,
        "record_type": "AAAA", "value": "", "format": "json", "record_line": "默认"}
]

# 从网络读取文件
def getwebip():
    logging.info("begin get web ip .")
    req = urllib2.Request("http://v6.ipv6-test.com/api/myip.php")
    reo = urllib2.urlopen(req)
    res = reo.read()
    reo.close()
    return res

# 从本地读取文件
def getlocip():
    logging.info("begin get local ip .")
    if not os.path.exists(_ipfile):
        return ''
    with open(_ipfile, 'r') as fo:
        return fo.readline()


def saveip(ip):
    logging.info("begin save ip .")
    with open(_ipfile, 'w') as fo:
        fo.write(ip)


def ddns(ip):
    try:
        for domain in domains:
            domain["value"] = ip
            req = urllib2.Request(
                "https://dnsapi.cn/Record.Modify", urllib.urlencode(domain))
            reo = urllib2.urlopen(req)
            res = reo.read()
            logging.info("update ["+domain['sub_domain']+"] res:" + res)
        return True
    except Exception, e:
        logging.error("update error:" + str(e))
        return False


if __name__ == '__main__':
    logging.info("start check ...")
    local_ip = getlocip()
    logging.info("local ip is : " + local_ip)
    try:
        ip = getwebip()
        logging.info("web ip is : " + ip)
        if local_ip != ip:
            logging.info("ip changed, begin request")
            if ddns(ip):
                saveip(ip)
        else:
            logging.info("ip not chang, wait next time")
    except Exception, e:
        logging.error(str(e))
        pass


# cls ; python2 dnspodv6_corn.py
