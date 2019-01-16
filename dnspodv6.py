#!/usr/bin/env python2
# -*- coding:utf-8 -*-


import time
import os
import json
import urllib
import urllib2

import logging
logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.ERROR)

# 详见 : https://support.dnspod.cn/Kb/showarticle/tsid/227/
login_token = "your_token"
# 详见 : https://www.dnspod.cn/docs/records.html#record-modify
domains = [
    {"login_token": login_token, "sub_domain": "sub1", "domain_id": 100, "record_id": 101,
        "record_type": "AAAA", "value": "", "format": "json", "record_line": "默认"},
    {"login_token": login_token, "sub_domain": "sub2", "domain_id": 102, "record_id": 103,
        "record_type": "AAAA", "value": "", "format": "json", "record_line": "默认"}
]


def getip():
    req = urllib2.Request("http://v6.ipv6-test.com/api/myip.php")
    reo = urllib2.urlopen(req)
    res = reo.read()
    reo.close()
    return res


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


local_ip = ''


def main():
    global local_ip
    logging.info("start check local ip ...")
    try:
        ip = getip()
        logging.info("local ip is : " + ip)
        if local_ip != ip:
            logging.info("ip changed, begin request")
            if ddns(ip):
                local_ip = ip
        else:
            logging.info("ip not chang, wait next time")
    except Exception, e:
        logging.error(str(e))
        pass


if __name__ == '__main__':
    while True:
        main()
        time.sleep(30)
