#!/usr/bin/env python
# coding: utf-8
#A Vulnerability Scanning tools
#mail: with.h4rdy@gmail.com

import json
import requests
import time
import threading
import Queue
import sys
import warnings
from optparse import OptionParser


warnings.filterwarnings("ignore")
json_database = 'database.json'
timeout = 3
allow_redirects = True
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'}
domain = Queue.Queue()


class Burst(threading.Thread):
    def __init__(self,domainqueue):
        threading.Thread.__init__(self)
        self.domain = domain

    def _burst_start(self, url, text, mold, result_dic):
        try:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=allow_redirects, verify=False)
            if r.status_code == requests.codes.ok:
                if text in r.content:
                    print url
                    self._deal_result(url, result_dic, mold)
                else:
                    pass
            else:
                pass  
        except:
            pass

    def _make_result_dic(self, mold):
        if mold in result_dic.keys():
            pass
        else:
            result_dic.setdefault(mold, [])
        return result_dic

    def _deal_result(self, url, result_dic, mold):
        a = result_dic.get(mold)
        a.append(url)
        result_dic.setdefault(mold, a)
        return result_dic

    def run(self, s):
        while self.domain.qsize() > 0:
            for i in xrange(0,int(len(s))):
                mold = database[i]["type"]
                self._make_result_dic(mold)
            host = self.domain.get(block=False)
            self.domain.task_done()
            if rules == "all":
                for i in xrange(0,int(len(database))):
                    mold = database[i]["type"]
                    path = database[i]["path"]
                    text = database[i]["text"]
                    msg =  "scanned in %.2f seconds\r"%(time.time()- start_time)
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                    url ="http://" +  host + path
                    self._burst_start(url, text, mold, result_dic)
            else:
                for i in xrange(0,int(len(database))):
                    mold = database[i]["type"]
                    for rule_num in range(0,len(rules.split(','))):
                        if mold == rules.split(',')[rule_num]:
                            path = database[i]["path"]
                            text = database[i]["text"]
                            msg =  "scanned in %.2f seconds\r"%(time.time()- start_time)
                            sys.stdout.write(msg)
                            sys.stdout.flush()
                            url ="http://" +  host + path 
                            self._burst_start(url, text, mold, result_dic)
        return result_dic


def save_result(result_dic, rules):
    if rules == "all":
        d = open(options.output_file+'.txt', 'a+')
        d.write(str(time.strftime("%Y-%m-%d %X", time.localtime())) + '\n\n')
        for k in result_dic.keys(): 
            d.write('['+k+']' + '\n')
            for i in range(0,len(result_dic.get(k))):
                d.write(result_dic.get(k)[i] + '\n')
            d.write('\n\n')
        d.close()
    else:
        d = open(options.output_file+'.txt', 'a+')
        d.write(str(time.strftime("%Y-%m-%d %X", time.localtime())) + '\n\n')
        for rule_num in range(0,len(rules.split(','))):
            d.write(rules.split(',')[rule_num] + '\n')
            try:
                for i in range(0,(len(result_dic.get(rules.split(',')[rule_num])))):
                    d.write(result_dic.get(rules.split(',')[rule_num])[i] + '\n')
            except:
                print 'Rule is error'
            d.write('\n\n')
        d.close()

if __name__ == '__main__':
    parser = OptionParser('usage: [target] or -f [target_file]')
    parser.add_option('-f', dest='target_file', type='string', help='The files path')
    parser.add_option('-t', dest='thread_num',  type='int', default=15, help='Number of threads. default = 20')
    parser.add_option('-o', dest='output_file', type='string', default='time''', help='Output file name.')
    parser.add_option('-r', dest='rules', type='string', default='all', help='Choice the rule.')
    
    (options, args) = parser.parse_args()
    rules = options.rules
    result_dic = {}
    start_time = time.time() 
    try:
        a = open(json_database)
        database = json.load(a)['json']  
    except:
        print 'open database.json error'
    if options.target_file is not None:
        f = open(options.target_file)
        for h in f.readlines():
            domain.put(h.strip())
        f.close()
        url_length =  int(domain.qsize())
        for i in xrange (options.thread_num):
            t = Burst(domain)
            t.run(database)
        domain.join()
        save_result(result_dic, rules)
    else:
        try:
            print args[0]
            url_length = 1
            t = Burst(domain.put(args[0]))
            t.run(database)
        except:
            parser.print_help()
