#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sqlite3
#说明
print u''
print u'-----------------使用说明-----------------'
print u'将脚本放入日志所在目录，运行脚本，输入日志\n文件名（含扩展名），将在相同目录生成log.db\n数据库'
print u'------------------------------------------'
print u''
#读取日志文件、连接数据库
name = raw_input('Please input the log name:')
log_db = sqlite3.connect('./log.db')
cursor = log_db.cursor()
#建表
cursor.execute('DROP TABLE IF EXISTS log')
cursor.execute('CREATE TABLE log (front, log_date, log_time, log_path, value, level)')
#设定正则规则
data_re = re.compile(r'(?P<front>[^:]+):\[(?P<log_date>[^\s]+)\s(?P<log_time>[^\]]+)\]\s+(?P<log_path>[^\|]+)\|\|(?P<value>\d+):(?P<level>\d+)',re.S|re.M)
#读取日志文件
log = open('./%s' %name)
index = 0
#进行转换
try:
    for line in log:
        found = data_re.findall(line)
        if found != None and len(found) != 0:
            index = index + 1
            cursor.execute('INSERT INTO log (front, log_date, log_time, log_path, value, level) VALUES (?,?,?,?,?,?)', (found[0][0], found[0][1], found[0][2], found[0][3], found[0][4], found[0][5]))
            if index == 100:
                log_db.commit()
                #print '100 records has been submitted.'
    log_db.commit()
    print 'job done!'
    input()
except:
    pass
